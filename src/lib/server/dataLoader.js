function loadCookie(cookies, key){
    try {
        const cookie = cookies.get(key);
        if(cookie){
            return JSON.parse(cookie);
        }
    } catch {
        // ignore bad JSON
    }
    return null;
}

export async function loadWeapons(fetch, cookies){
    const res = await fetch('/helldivers_weapons.json');
    const weapons = await res.json();

    const checkedUrls = loadCookie(cookies, 'checkedWeapons');
    const selectedItems = loadCookie(cookies, 'selectedItems');
    const lockedItems = loadCookie(cookies, 'lockedItems');

    const urlSet = new Set(checkedUrls ?? []);
    weapons.forEach(w => {
        w.checked = checkedUrls == null || urlSet.has(w.id);
    });
  
    return { 
        weapons,
        selectedItems,
        lockedItems
    };
}