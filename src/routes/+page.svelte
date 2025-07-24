<script>
    import IconDice from 'virtual:icons/ion/dice';
    import IconLockOpen from 'virtual:icons/ion/lock-open';
    import IconLockClosed from 'virtual:icons/ion/lock-closed';
    import IconList from 'virtual:icons/ion/list';
    import IconSettings from 'virtual:icons/ion/settings';
	import _ from "lodash";
	import { pickRandom, setCookie } from '$lib/constants.js';
	import StratagemPool from '$lib/stratagemPool.js';

    let { data } = $props();

    const weapons = data.weapons;
    const weaponLookup = _.keyBy(weapons, "id");

    function filterByCategory(category) {
        return weapons.filter(
            p => p.category === "Weapon" && p.extra?.weapon_category === category
        );
    }

    const ordinarySlots = ['primary', 'secondary', 'grenade', 'booster'];
    const stratagemSlots = ["stratagem_0", "stratagem_1", "stratagem_2", "stratagem_3"];

    const available = {
        "primary": filterByCategory("Primary Weapons"),
        "secondary": filterByCategory("Secondary Weapons"),
        "grenade": filterByCategory("Grenades"),
        "stratagem": weapons.filter(p => p.category === "Stratagem"),
        "booster": weapons.filter(p => p.category === "Booster")
    }

    function loadSelectedItems(){
        if(!data.selectedItems) return;
        try{

            const mapped = _.mapValues(data.selectedItems, p => weaponLookup[p]);
            return mapped;

        }catch(err){
        }

        return;
    }

    let selected = $state(loadSelectedItems() ?? {});
    let locked = $state(data.lockedItems ?? {});

    function saveSelectedItems(){
        setCookie("selectedItems", _.mapValues(selected, "id"));
    }
    
    function saveLockedItems(){
        setCookie("lockedItems", locked);
    }

    function toggleLock(slot) {
        locked[slot] = !locked[slot];
        saveLockedItems();
    }

    function getSlot(slot){
        return slot.split("_")[0];
    }

    function getAvailableItems(slot){
        return available[getSlot(slot)].filter(p => p.checked);
    }

    function reroll(slot, save=true) {
        if (locked[slot]) return;

        // This function is normally only called for ordinary slots.
        // If it's called for a stratagem slot, that means it's a single-slot
        // re-roll. For stratagems, this requires special handling, since
        // there are multiple of them that should avoid duplicates,
        // and abide to any group restrictions.
        if(slot.startsWith("stratagem")){
            const pool = getStratagemPool(slot);
            selected[slot] = pool.pickNext();
            saveSelectedItems();
            return;
        }

        let pool = getAvailableItems(slot);

        console.log("Picking " + slot + " from pool of " + pool.length + " items.");

        selected[slot] = pickRandom(pool) ?? undefined;

        if(save){
            saveSelectedItems();
        }
    }

    /** Returns the pool of stratagems that are available for picking.
     * If this is a full re-roll, that means all stratagems minus the locked ones.
     * If this is a single-slot re-roll, that means all stratagems minus the other ones.
     * @param {string} singleSlot - Set to the slot we are picking for if we are only picking a single stratagem (the three other already picked stratagems will be removed from the pool)
     */
    function getStratagemPool(singleSlot=null){
        
        // Start with the full stratagem pool, and set it up
        // to pick items abiding the group restrictions (if any).
        const pool = new StratagemPool(getAvailableItems("stratagem"), Object.values(data.groups));

        for(const slot of stratagemSlots){

            // If this is the slot we are picking for, it will be re-rolled -- ignore the picked item.
            if(singleSlot == slot) continue;

            // If this is a full re-roll, and this slot is not locked, it will be re-rolled -- ignore the picked item.
            if(!singleSlot && !locked[slot]) continue;

            // Otherwise, if this is a single-slot pick, or if this item is locked, we need 
            // to remove it from the available pool.
            pool.picked(selected[slot]);
        }
        return pool;
    }

    function rerollAll() {
        ordinarySlots.forEach(p => reroll(p, false));

        const stratagemPool = getStratagemPool();
        for(const slot of stratagemSlots){
            if(locked[slot]) continue;
            selected[slot] = stratagemPool.pickNext();
        }

        saveSelectedItems();
    }

    if(!data.selectedItems || !data.lockedItems){
        rerollAll();
    }

    function describeRule(rule){
        if(rule.min == rule.max){
            return "Pick exactly " + rule.min + " items.";
        }
        if(rule.min > 0 && rule.max < 4){
            return "Pick at least " + rule.min + " items, but not more than " + rule.max + ".";
        }
        if(rule.min > 0){
            return "Pick at least " + rule.min + " items.";
        }
        if(rule.max < 4){
            return "Pick at most " + rule.max + " items.";
        }
        return "Pick freely.";
    }
</script>

{#snippet ContainerHeader(slot, customTitle = null)}
    <div class="flex flex-row gap-3 items-center">
        <h2 class="text-sm md:text-xl font-bold capitalize">{customTitle ?? slot}</h2>
    </div>
{/snippet}

{#snippet WeaponContainer(slot, showHeader = true)}
    <div class="relative text-sm sm:text-base">
        <button
            class="w-full cursor-pointer text-center rounded-lg p-4 hover:bg-gray-100 transition flex flex-col justify-between items-center {showHeader ? "h-44 sm:h-64" : "h-32 sm:h-44"}" class:border={showHeader}
            onclick={() => reroll(slot)} data-umami-event="reroll-single-{slot.split("_")[0]}"
        >
            {#if showHeader}
                {@render ContainerHeader(slot)}
            {/if}
            {#if selected[slot]}
                <div class="flex-1 flex justify-center {showHeader ? "items-center" : "items-start"}">
                    <img src={selected[slot].icon_file} alt={selected[slot].name} class="max-h-16 md:max-h-24" />
                </div>
                <p class="text-xs sm:text-base mt-2">{selected[slot].name}</p>
            {:else if selected[slot] == undefined}
                <p>No items available.</p>
            {:else}
                <p>Loading...</p>
            {/if}
        </button>
        <button class="absolute top-1 right-1 sm:top-2 sm:right-2 cursor-pointer" title="Tap to lock this item from re-rolling" onclick={() => toggleLock(slot)} data-umami-event="toggle-lock-{slot}">
            {#if locked[slot]}
                <IconLockClosed />
            {:else}
                <IconLockOpen />
            {/if}
        </button>
    </div>
{/snippet}

<div class="max-w-6xl mx-auto px-4 py-10">

    <div class="grid grid-cols-4 gap-2 sm:gap-6 mb-10">
        {#each ordinarySlots as slot}
            {@render WeaponContainer(slot)}
        {/each}
    </div>

    <div class="border rounded-lg p-4 mb-10">
        <div class="flex flex-row items-center justify-center mb-5">
            {@render ContainerHeader("Stratagem", "Stratagems")}
        </div>
        <div class="grid grid-cols-4 gap-2 sm:gap-6">
            {#each stratagemSlots as slot}
                {@render WeaponContainer(slot, false)}
            {/each}
        </div>
    </div>

    <div class="flex justify-center gap-10">
        <button class="bg-blue-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onclick={rerollAll} data-umami-event="reroll-all">
            <IconDice class="inline-block mr-1 text-2xl" /> Reroll All
        </button>
    </div>

    <!-- Make the browser pre-load all images so that updates are instant when re-rolling. -->
    <div class="hidden">
        {#each weapons.filter(p => p.checked) as weapon}
            <img src={weapon.icon_file} alt={weapon.name} width="1" height="1" loading="eager" />
        {/each}
    </div>
</div>

<div class="mt-10 py-10 bg-gray-200">
    <div class="flex flex-row flex-wrap justify-center gap-10">
        <div class="text-center md:text-right w-96">
            <h2 class="text-2xl">Items</h2>
            <table class="inline-block">
                <thead></thead>
                <tbody>
                    {#each ordinarySlots.concat(["stratagem"]) as slot}
                        {@const have = available[slot]?.filter(p => p.checked).length ?? "?"}
                        {@const total = available[slot]?.length ?? "?"}
                        <tr>
                            <td class="pr-5">{slot}</td>
                            <td>
                                {#if have == total}
                                    all ({total})
                                {:else}
                                    {have} / {total}
                                {/if}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
        <div class="text-center md:text-left w-96">
            <h2 class="text-2xl">Rules</h2>
            {#each Object.values(data.groups).filter(p => p.enabled && (p.min > 0 | p.max < 4)) as rule}
                <div>
                    {rule.title}:
                    {describeRule(rule)}
                </div>
            {:else}
                <div>No group restrictions.</div>
            {/each}
        </div>
    </div>

    <div class="flex justify-center gap-10 mt-10">
        <a class="bg-green-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-green-700 transition cursor-pointer" data-umami-event="items-button" href="/items">
            <IconList class="inline-block mr-1 text-2xl" /> Items
        </a>
        <a class="bg-green-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-green-700 transition cursor-pointer" data-umami-event="options-button" href="/rules">
            <IconSettings class="inline-block mr-1 text-2xl" /> Rules
        </a>
    </div>
</div>

<div class="py-10 flex flex-col text-center gap-2">
    <h2 class="text-2xl">About</h2>
    <p>A simple and open source tool for picking random Helldivers 2 loadouts.</p>
    <p>Uses cookies to store your item selection and ruleset.</p>
    <p><a class="underline" target="_blank" href="https://github.com/erlenddahl/stratagem-picker" data-umami-event="github-link">Help me improve it on Github</a></p>
</div>

<style>
    img {
        max-width: 100%;
        height: auto;
    }
</style>