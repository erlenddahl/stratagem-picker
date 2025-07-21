# Weapon Data Extractor for Stratagem Picker

This script extracts weapon data from [helldivers.wiki.gg](https://helldivers.wiki.gg), downloads their icons, generates thumbnails, and saves everything in a structured format for use in the Stratagem Picker project.

> ⚠️ **Note:** This script is mostly AI-generated and intended to be run rarely. It works, but hasn't been cleaned up or optimized. Use at your own convenience.

---

## 📦 Setup

You should run this in an isolated Python environment -- for example, using Conda.

### 1. Create and activate a virtual environment (example using Conda):

```bash
conda create -n stratagem-picker python=3.10
conda activate stratagem-picker
```

### 2. Install dependencies:

Install required Python packages using the included `requirements.txt` file:

```bash
pip install -r requirements.txt
```

> 💡 **SVG support:**  
> This script uses [`wand`](https://github.com/emcconville/wand) to convert `.svg` images to `.png`.  
> You must also install [ImageMagick](https://imagemagick.org/script/download.php) and ensure it is available in your system `PATH`.

When installing ImageMagick:
- ✅ Check "Add application directory to your system PATH"
- ✅ Enable "Install legacy utilities (e.g. convert)"

---

## ▶️ Usage

From the project root directory, run:

```bash
python extractor.py
```

The script will:

- Fetch and parse weapon data from the wiki
- Download and crop `.png` or `.svg` icons
- Save icons and scaled thumbnails (max size: 315×125 px)
- Return structured weapon data

---

## 📂 Output

- Icons are saved to the `ICON\_DIR` defined in the script.
- Thumbnails are saved to the `THUMB\_DIR` defined in the script.
- SVGs are converted to PNG before processing.
