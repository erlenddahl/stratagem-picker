import os
import re
import json
import time
import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from PIL import Image, ImageChops, ImageOps
from io import BytesIO
from wand.image import Image as WandImage

class SoupFetcher:
    def __init__(self, page_delay = 0):
        self.driver = uc.Chrome() 
        self.page_delay = page_delay

    def get_soup(self, url):
        print(f"\nFetching: {url}")
        self.driver.get(url)

        time.sleep(self.page_delay)

        while "Security checks are being performed by" in self.driver.page_source:
            print("Waiting for Cloudflare verification, please solve in browser...")
            time.sleep(1)

        return BeautifulSoup(self.driver.page_source, "html.parser")

    def close(self):
        self.driver.quit()

ROOT_URL = "https://helldivers.wiki.gg"
WEAPON_URL = "https://helldivers.wiki.gg/wiki/Weapons"
STRATAGEM_URL = "https://helldivers.wiki.gg/wiki/Stratagems"
BOOSTER_URL = "https://helldivers.wiki.gg/wiki/Boosters"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}
ICON_DIR = "images"
THUMB_DIR = "thumbs"
OUTPUT_FILE = "helldivers_weapons.json"

os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)
weapons = []

def sanitize_filename(name):
    return name.replace(" ", "_").replace("/", "_").replace("\"", "_") \
               .replace(":", "_").replace("?", "_").replace("!", "_")

def download_icon(name, icon_url):
    if not name:
        raise Exception("Empty name!")
    filename = sanitize_filename(f"{name}.png")
    icon_path = os.path.join(ICON_DIR, filename)
    if not os.path.isfile(icon_path):
        try:
            img_data = requests.get(icon_url, headers=HEADERS).content
            
            if ".svg" in icon_url.lower():
                with WandImage(blob=img_data, format='svg') as wand_img:
                    wand_img.format = 'png'
                    png_data = wand_img.make_blob()
                img = Image.open(BytesIO(png_data)).convert("RGBA")
            else:
                img = Image.open(BytesIO(img_data)).convert("RGBA")

            # Step 1: Flatten onto a white background to handle white border detection
            flattened = Image.new("RGBA", img.size, (255, 255, 255, 255))
            flattened.paste(img, mask=img.split()[3])  # paste using alpha as mask

            # Step 2: Convert to RGB and trim using white background
            rgb = flattened.convert("RGB")
            bg = Image.new("RGB", rgb.size, (255, 255, 255))
            diff = ImageChops.difference(rgb, bg)
            bbox = diff.getbbox()

            # Step 3: Crop both original RGBA and flattened image using bounding box
            if bbox:
                img = img.crop(bbox)

            img.save(icon_path, format="PNG")

            # Save a scaled-down thumbnail within 315x125 (without enlarging)
            thumb_path = os.path.join(THUMB_DIR, sanitize_filename(f"{name}.png"))
            thumb_img = img.copy()
            thumb_img.thumbnail((315, 125), Image.LANCZOS)
            thumb_img.save(thumb_path, format="PNG")

            time.sleep(0.1)
        except Exception as e:
            print(f"    ⚠️ Failed to download icon '{icon_url}': {e}")
            return icon_url
    else:
        print(f"    ✅ Icon already downloaded")
    return icon_path

def has_weapon(url):
    return any(w.get("url") == url for w in weapons)

def append_weapon_data(name, url, icon_url, warbond, category, weapon_type, icon_path, extra=None):

    if has_weapon(url):
        print("    ⚠️ Skipped (already exists)")
        return

    weapons.append({
        "id": len(weapons),
        "name": name, 
        "icon_url": icon_url, 
        "icon_file": icon_path,
        "thumb_file": icon_path.replace(ICON_DIR, THUMB_DIR),
        "warbond": warbond.replace("Liberty Day 2184", "Patriotic Administration Center").replace(" Premium", "").replace("Premium Warbond: ", "").replace("Warbond: ", "").replace(" Warbond", "").replace(" warbond", "").replace("Page 1", "").replace("Page 2", "").replace("Purchased in Superstore", "Superstore").replace("Page 3", "").replace("()", "").replace("!", "").replace("freedom", "Freedom").replace("legends", "Legends").replace("Killzone Crossover", "Other").replace("Killzone collaboration", "Other").strip() if warbond else "None", 
        "category": category,
        "weapon_type": weapon_type, 
        "url": url,
        "extra": extra
    })

    print("    ✅ Added")

def set_detail(extra, details_soup, key):

    div = details_soup.find('div', attrs={'data-source': key})
    value = div.find("div").get_text(separator=" ", strip=True) if div else ""

    if value:
        extra[key] = value
        return True
    else:
        return False

def load_details(fetcher, url):
    details_soup = fetcher.get_soup(url)
    unlock_div = details_soup.find('div', attrs={'data-source': 'unlock_cost'})
    warbond = ""

    if unlock_div:

        warbond_links = [
            a.get_text(separator=" ", strip=True)
            for a in unlock_div.find_all('a', href=True)
            if "/wiki/Medal" not in a["href"] and "/wiki/Requisition_Slips" not in a["href"]
        ]

        warbond = warbond_links[0] if len(warbond_links) else ""

    if not warbond:

        unlock_div = details_soup.find('div', attrs={'data-source': 'source'})
        
        if unlock_div:
        
            warbond_links = [
                a.get_text(separator=" ", strip=True)
                for a in unlock_div.find_all('a', href=True)
            ]

            warbond = warbond_links[0] if len(warbond_links) else ""

    if not warbond:
        print(f"    ⚠️ missing warbond info")
    else:
        print(f"    ✅ warbond: {warbond}")

    extra = {}

    if set_detail(extra, details_soup, 'traits') or set_detail(extra, details_soup, 'weapon_traits'):
        if "weapon_traits" in extra:
            extra["traits"] = extra["weapon_traits"]
            del extra["weapon_traits"]
        extra["traits"] = [x.strip() for x in extra["traits"].split("•")]

    set_detail(extra, details_soup, 'ship_module')
    set_detail(extra, details_soup, 'weapon_category')
    set_detail(extra, details_soup, 'weapon_type')
    set_detail(extra, details_soup, 'penetration')
    set_detail(extra, details_soup, 'source')
    set_detail(extra, details_soup, 'permit_type')

    return warbond, extra

def load_weapons(fetcher):
    soup = fetcher.get_soup(WEAPON_URL)
    mc = soup.select_one("div#mw-content-text")
    if not mc: raise RuntimeError("Could not find main content.")
    
    for row in mc.find_all('li', class_="gallerybox"):
        link = row.find("div", class_="gallerytext").find("a")
        name = link.get_text(strip=True)
        url = ROOT_URL + link["href"]
        icon = row.find("img")
        icon_url = ROOT_URL + icon.get("src")

        if has_weapon(url):
            print("    ⚠️ Skipped (already exists)")
            continue

        icon_path = download_icon(name, icon_url)
        warbond, extra = load_details(fetcher, url)

        append_weapon_data(name, url, icon_url, warbond, "Weapon", "", icon_path, extra)

def convert_thumb_to_original(url):
    url = url.replace("/thumb", "")
    url = url.split("/50px-")[0]
    url += "?format=original"
    return url

def load_stratagems(fetcher):
    soup = fetcher.get_soup(STRATAGEM_URL)
    table = soup.find("table", class_="wikitable")
    if not table: 
        raise RuntimeError("Could not find boosters table.")

    current_type = ""

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells or len(cells) < 7:
            print(f"    invalid row")
            continue

        offset = 0
        if len(cells) == 8:
            current_type = cells[0].get_text(separator=" ", strip=True)
            offset = 1

        name = cells[1 + offset].get_text(separator=" ", strip=True)
        link = cells[1 + offset].find("a")
        icon = cells[0 + offset].find("img")

        if not link:
            print(f"    ⚠️ missing link")

        if not name:
            print(f"    ⚠️ missing name")

        if not icon:
            print(f"    ⚠️ missing icon")

        href = ROOT_URL + link.get("href")
        icon_url = ROOT_URL + icon.get("src") if icon is not None else ""
        if "/thumb/" in icon_url:
            icon_url = convert_thumb_to_original(icon_url)
        icon_path = download_icon(name, icon_url)

        if has_weapon(href):
            print("    ⚠️ Skipped (already exists)")
            continue

        warbond, extra = load_details(fetcher, href)

        append_weapon_data(name, href, icon_url, warbond, "Stratagem", current_type, icon_path, extra)

def load_boosters(fetcher):
    soup = fetcher.get_soup(BOOSTER_URL)
    table = soup.find("table", class_="wikitable")
    if not table: raise RuntimeError("Could not find boosters table.")

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells or len(cells) < 4:
            print(f"    invalid row")
            continue

        name = cells[1].get_text(separator=" ", strip=True)
        link = cells[1].find("a")
        icon = cells[0].find("img")
        warbond = cells[3].get_text(separator=" ", strip=True)

        if not link:
            print(f"    ⚠️ missing link")

        if not name:
            print(f"    ⚠️ missing name")

        if not warbond:
            print(f"    ⚠️ missing warbond")

        if not icon:
            print(f"    ⚠️ missing icon")

        icon_url = ROOT_URL + icon.get("src") if icon is not None else ""
        href = ROOT_URL + link.get("href")

        if has_weapon(href):
            print("    ⚠️ Skipped (already exists)")
            continue

        icon_path = download_icon(name, icon_url)
        append_weapon_data(name, href, icon_url, warbond, "Booster", "", icon_path)

def find(name):

    for w in weapons:
        if w["name"] == name:
            return w
    return None

def set_custom_data():
    
    for item in weapons:
        if item["extra"] and item["extra"].get("ship_module") == "Patriotic Administration Center":
            item["warbond"] = "Patriotic Administration Center"
        
        if (not item["warbond"] or item["warbond"] == "None") and item["extra"] and item["extra"].get("ship_module") == "Orbital Cannons":
            item["warbond"] = "Orbital Cannons"
        if (not item["warbond"] or item["warbond"] == "None") and item["extra"] and item["extra"].get("ship_module") == "Hangar":
            item["warbond"] = "Hangar"
        if (not item["warbond"] or item["warbond"] == "None") and item["extra"] and item["extra"].get("ship_module") == "Bridge":
            item["warbond"] = "Bridge"
        if (not item["warbond"] or item["warbond"] == "None") and item["extra"] and item["extra"].get("ship_module") == "Engineering Bay":
            item["warbond"] = "Engineering Bay"
        if (not item["warbond"] or item["warbond"] == "None") and item["extra"] and item["extra"].get("ship_module") == "Robotics Workshop":
            item["warbond"] = "Robotics Workshop"
        
        if item["extra"] and item["extra"].get("source") == "Starter Equipment":
            item["warbond"] = "Patriotic Administration Center"
        if "killzone" in item["warbond"].lower() or "liberty day" in item["warbond"].lower() or "superstore" in item["warbond"].lower() or "super citizen edition" in item["warbond"].lower():
            item["warbond"] = "Other"

        manual = {
            "https://helldivers.wiki.gg/wiki/P-92_Warrant": "Force of Law",
            "https://helldivers.wiki.gg/wiki/P-11_Stim_Pistol": "Chemical Agents",
            "https://helldivers.wiki.gg/wiki/TED-63_Dynamite": "Borderline Justice",
            "https://helldivers.wiki.gg/wiki/G-10_Incendiary": "Steeled Veterans",
            "https://helldivers.wiki.gg/wiki/PLAS-39_Accelerator_Rifle": "Other",
            "https://helldivers.wiki.gg/wiki/G-6_Frag": "Helldivers Mobilize",
            "https://helldivers.wiki.gg/wiki/G-16_Impact": "Helldivers Mobilize",
            "https://helldivers.wiki.gg/wiki/G-13_Incendiary_Impact": "Polar Patriots",
            "https://helldivers.wiki.gg/wiki/G-23_Stun": "Cutting Edge",
            "https://helldivers.wiki.gg/wiki/G-4_Gas": "Chemical Agents",
            "https://helldivers.wiki.gg/wiki/G-50_Seeker": "Servants of Freedom",
            "https://helldivers.wiki.gg/wiki/G-3_Smoke": "Helldivers Mobilize",
            "https://helldivers.wiki.gg/wiki/G-123_Thermite": "Democratic Detonation",
            "https://helldivers.wiki.gg/wiki/K-2_Throwing_Knife": "Viper Commandos",
            "https://helldivers.wiki.gg/wiki/G-142_Pyrotech": "Masters of Ceremony",
            "https://helldivers.wiki.gg/wiki/G-109_Urchin": "Force of Law",
            "https://helldivers.wiki.gg/wiki/G-31_Arc": "Control Group",
            "https://helldivers.wiki.gg/wiki/G-12_High_Explosive": "Patriotic Administration Center",
            "https://helldivers.wiki.gg/wiki/CQC-1_One_True_Flag": "Masters of Ceremony",
            "https://helldivers.wiki.gg/wiki/E/GL-21_Grenadier_Battlement": "Bridge"
        }

        mapped_warbond = manual.get(item["url"], None)
        if mapped_warbond:
            item["warbond"] = mapped_warbond

        disabled_items = [
            "https://helldivers.wiki.gg/wiki/SG-88_Break-Action_Shotgun",
            "https://helldivers.wiki.gg/wiki/Entrenchment_Tool"
        ]

        if item["name"].startswith("G-"):
            item["extra"]["weapon_category"] = "Grenades"

        if item["url"] in disabled_items:
            item["disabled"] = True

def main():

    global weapons

    fetcher = SoupFetcher(1)

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        weapons = json.load(f)

    print(f"\n🔧 Loaded items: {len(weapons)}")

    load_stratagems(fetcher)
    load_weapons(fetcher)
    load_boosters(fetcher)

    set_custom_data()

    print(f"\n🔧 Found total items: {len(weapons)}. Saving...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(weapons, f, indent=2, ensure_ascii=False)
    print(f"✅ Done. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
