export async function loadWeapons(fetch, cookies){
    const res = await fetch('/helldivers_weapons.json');
    const weapons = await res.json();

    let checkedUrls = [];

    try {
        const cookie = cookies.get('checkedWeapons');
        if(cookie){
            checkedUrls = cookie ? JSON.parse(cookie) : [];
        }else{
            checkedUrls = null;
        }
    } catch {
        // ignore bad JSON
    }

    const urlSet = new Set(checkedUrls ?? []);
    weapons.forEach(w => {
        w.checked = checkedUrls == null || urlSet.has(w.id);
    });
  
    return { 
        weapons
    };
}