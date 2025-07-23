import { getGroups } from "$lib/constants";

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
    const groupSettings = loadCookie(cookies, "groups") ?? [
        {
            id: "anti-tanks",
            enabled: true,
            min: 1,
            max: 4
        },
        {
            id: "backpacks",
            enabled: true,
            min: 0,
            max: 1
        }
    ];

    const urlSet = new Set(checkedUrls ?? []);
    weapons.forEach(w => {
        w.checked = checkedUrls == null || urlSet.has(w.id);
    });

    const groups = getGroups(weapons);
    for(const setting of groupSettings){
        const g = groups[setting.id];
        if(!g) return;
        g.enabled = setting.enabled;
        g.min = setting.min;
        g.max = setting.max;
    }
  
    return { 
        weapons,
        selectedItems,
        lockedItems,
        groups
    };
}