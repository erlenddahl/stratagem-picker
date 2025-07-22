import { browser } from '$app/environment';

export const warbondSortOrder = [
    "Patriotic Administration Center",
    "Orbital Cannons",
    "Bridge",
    "Robotics Workshop",
    "Engineering Bay",
    "Hangar",
    "Other",
    "Helldivers Mobilize",
    "Steeled Veterans",
    "Cutting Edge",
    "Democratic Detonation",
    "Polar Patriots",
    "Viper Commandos",
    "Freedom's Flame",
    "Chemical Agents",
    "Truth Enforcers",
    "Urban Legends",
    "Servants of Freedom",
    "Borderline Justice",
    "Masters of Ceremony",
    "Force of Law",
    "Control Group"
];

export function getGroups(weapons){
    const groups = {
        "anti-tanks": {
            title: "Anti-tank weapons",
            items: weapons.filter(p => p.extra?.weapon_category == "Support Weapons" && p.extra?.traits?.indexOf("Anti-Tank") >= 0)
        },
        "eagles": {
            title: "Eagle strikes",
            items: weapons.filter(p => p.extra?.traits?.indexOf("Eagle") >= 0)
        },
        "barrages": {
            title: "Barrages",
            items: weapons.filter(p => p.name.toLowerCase().indexOf("barrage") >= 0)
        },
        "vehicles": {
            title: "Vehicles",
            items: weapons.filter(p => p.extra?.traits?.indexOf("Vehicle") >= 0)
        },
        "missiles": {
            title: "Missile weapons",
            items: weapons.filter(p => p.extra?.weapon_type == "Missiles")
        },
        "sentries": {
            title: "Sentries",
            items: weapons.filter(p => p.extra?.traits?.indexOf("Sentry") >= 0)
        },
        "emplacements": {
            title: "Emplacements",
            items: weapons.filter(p => p.extra?.weapon_category == "Emplacement")
        },
        "backpacks": {
            title: "Backpacks",
            items: weapons.filter(p => p.extra?.traits?.indexOf("Backpack") >= 0)
        }
    }

    for(const key of Object.keys(groups)){
        groups[key].id = key;
    }

    return groups;
}

export function pickRandom(list) {
    return list[Math.floor(Math.random() * list.length)];
}

export function setCookie(key, value){
    if(!browser) return;
    const encoded = encodeURIComponent(JSON.stringify(value));
    document.cookie = `${key}=${encoded}; path=/; max-age=31536000`;
}