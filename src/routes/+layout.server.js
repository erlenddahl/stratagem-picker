export async function load({ fetch, cookies }) {
    const res = await fetch('/helldivers_weapons.json');
    const weapons = await res.json();

    let checkedUrls = [];

    try {
        const cookie = cookies.get('checkedWeapons');
        checkedUrls = cookie ? JSON.parse(cookie) : [];
    } catch {
        // ignore bad JSON
    }

    const urlSet = new Set(checkedUrls);
    weapons.forEach(w => {
        w.checked = urlSet.has(w.id);
    });
  
    return { 
        weapons
    };
}