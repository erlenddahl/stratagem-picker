import { loadWeapons } from '$lib/server/dataLoader.js';
import changelog from '$lib/itemChangelog.json';

export async function load({ fetch, cookies }) {
    return { ...(await loadWeapons(fetch, cookies)), changelog };
}
