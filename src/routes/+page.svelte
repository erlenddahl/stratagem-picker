<script>
    import IconDice from 'virtual:icons/ion/dice';
    import IconLockOpen from 'virtual:icons/ion/lock-open';
    import IconLockClosed from 'virtual:icons/ion/lock-closed';
    import IconList from 'virtual:icons/ion/list';
	import _ from "lodash";
    import { browser } from '$app/environment';

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

    function pickRandom(list) {
        return list[Math.floor(Math.random() * list.length)];
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
        if(!browser) return;
        const selectedItems = encodeURIComponent(JSON.stringify(_.mapValues(selected, "id")));
        document.cookie = `selectedItems=${selectedItems}; path=/; max-age=31536000`;
    }
    
    function saveLockedItems(){
        if(!browser) return;
        const lockedItems = encodeURIComponent(JSON.stringify(locked));
        document.cookie = `lockedItems=${lockedItems}; path=/; max-age=31536000`;
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

    function reroll(slot, save=true, predefined_pool=null) {
        if (locked[slot]) return predefined_pool;

        let pool = predefined_pool ?? (slot.startsWith("stratagem_") ? getStratagemPool(slot) : getAvailableItems(slot));

        console.log("Picking " + slot + " from pool of " + pool.length + " items.");

        selected[slot] = pickRandom(pool) ?? undefined;

        if(save){
            saveSelectedItems();
        }

        if(predefined_pool){
            return predefined_pool.filter(p => p.id != selected[slot]?.id);
        }
    }

    function getStratagemPool(singleSlot=null){
        let stratagemPool = getAvailableItems("stratagem");
        for(const slot of stratagemSlots){
            if(singleSlot == slot) continue;
            if(!singleSlot && !locked[slot]) continue;
            stratagemPool = stratagemPool.filter(p => p.id != selected[slot]?.id);
        }
        return stratagemPool;
    }

    function rerollAll() {
        ordinarySlots.forEach(p => reroll(p, false));

        let stratagemPool = getStratagemPool();
        for(const slot of stratagemSlots){
            if(locked[slot]) continue;
            stratagemPool = reroll(slot, false, stratagemPool);
        }

        saveSelectedItems();
    }

    if(!data.selectedItems || !data.lockedItems){
        rerollAll();
    }
</script>

{#snippet ContainerHeader(slot, customTitle = null)}
    {@const shortSlot = slot.toLowerCase().split("_")[0]}
    {@const have = available[shortSlot]?.filter(p => p.checked).length ?? "?"}
    {@const total = available[shortSlot]?.length ?? "?"}
    <div class="flex flex-row gap-3 items-center">
        <h2 class="text-xl font-bold capitalize">{customTitle ?? slot}</h2>
        <span class="text-sm" title="You have {have} of {total} items in this category">[{have} / {total}]</span>
    </div>
{/snippet}

{#snippet WeaponContainer(slot, showHeader = true)}
    <div class="relative">
        <button
            class="w-full cursor-pointer text-center rounded-lg p-4 hover:bg-gray-100 transition flex flex-col justify-between items-center {showHeader ? "h-72" : "h-52"}" class:border={showHeader}
            onclick={() => reroll(slot)}
        >
            {#if showHeader}
                {@render ContainerHeader(slot)}
            {/if}
            {#if selected[slot]}
                <div class="flex-1 flex justify-center {showHeader ? "items-center" : "items-start"}">
                    <img src={selected[slot].icon_file} alt={selected[slot].name} class="max-h-32" />
                </div>
                <p class="text-lg mt-2">{selected[slot].name}</p>
            {:else if selected[slot] == undefined}
                <p>No items available.</p>
            {:else}
                <p>Loading...</p>
            {/if}
        </button>
        <button class="absolute top-2 right-2 cursor-pointer" title="Tap to lock this item from re-rolling" onclick={() => toggleLock(slot)}>
            {#if locked[slot]}
                <IconLockClosed />
            {:else}
                <IconLockOpen />
            {/if}
        </button>
    </div>
{/snippet}

<div class="max-w-6xl mx-auto px-4 py-10">

    <div class="grid grid-cols-4 gap-6 mb-10">
        {#each ordinarySlots as slot}
            {@render WeaponContainer(slot)}
        {/each}
    </div>

    <div class="border rounded-lg p-4 mb-10">
        <div class="flex flex-row items-center justify-center mb-5">
            {@render ContainerHeader("Stratagem", "Stratagems")}
        </div>
        <div class="grid grid-cols-4 gap-6">
            {#each stratagemSlots as slot}
                {@render WeaponContainer(slot, false)}
            {/each}
        </div>
    </div>

    <div class="flex justify-center gap-10">
        <button class="bg-blue-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onclick={rerollAll}>
            <IconDice class="inline-block mr-1 text-2xl" /> Reroll All
        </button>
        <a class="bg-green-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-green-700 transition cursor-pointer" href="/warbonds">
            <IconList class="inline-block mr-1 text-2xl" /> Select available items
        </a>
    </div>

    <!-- Make the browser pre-load all images so that updates are instant when re-rolling. -->
    <div class="hidden">
        {#each weapons.filter(p => p.checked) as weapon}
            <img src={weapon.icon_file} alt={weapon.name} width="1" height="1" loading="eager" />
        {/each}
    </div>
</div>

<style>
    img {
        max-width: 100%;
        height: auto;
    }
</style>