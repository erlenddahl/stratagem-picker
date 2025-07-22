import { loadWeapons } from '$lib/server/dataLoader.js';

export async function load({ fetch, cookies }) {
    return await loadWeapons(fetch, cookies);
}