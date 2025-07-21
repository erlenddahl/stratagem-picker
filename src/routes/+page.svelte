<script>
    import IconDice from 'virtual:icons/ion/dice';
    import IconLockOpen from 'virtual:icons/ion/lock-open';
    import IconLockClosed from 'virtual:icons/ion/lock-closed';
    import IconList from 'virtual:icons/ion/list';
	import _ from "lodash";

    let { data } = $props();

    const weapons = data.weapons;
    const weaponLookup = _.keyBy(weapons, "id");

    function filterByCategory(category) {
        return weapons.filter(
            p => p.category === "Weapon" && p.extra?.weapon_category === category
        );
    }

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

    function pickMany(list, count) {
        const copy = [...list];
        const result = [];
        for (let i = 0; i < count && copy.length > 0; i++) {
            const index = Math.floor(Math.random() * copy.length);
            result.push(copy.splice(index, 1)[0]);
        }
        return result;
    }

    function loadSelectedItems(){
        if(!data.selectedItems) return;
        try{

            const mapped = _.mapValues(data.selectedItems, p => weaponLookup[p]);

            console.log(data.selectedItems, mapped);

            return mapped;

        }catch(err){
        }

        return;
    }

    let selected = $state(loadSelectedItems() ?? {
        primary: null,
        secondary: null,
        grenade: null,
        stratagem_0: null,
        stratagem_1: null,
        stratagem_2: null,
        stratagem_3: null,
        booster: null
    });

    let locked = $state(data.lockedItems ?? {
        primary: false,
        secondary: false,
        grenade: false,
        stratagem_0: false,
        stratagem_1: false,
        stratagem_2: false,
        stratagem_3: false,
        booster: false
    });

    function saveSelectedItems(){
        const selectedItems = encodeURIComponent(JSON.stringify(_.mapValues(selected, "id")));
        document.cookie = `selectedItems=${selectedItems}; path=/; max-age=31536000`;
    }
    
    function saveLockedItems(){
        const lockedItems = encodeURIComponent(JSON.stringify(locked));
        document.cookie = `lockedItems=${lockedItems}; path=/; max-age=31536000`;
    }

    function toggleLock(slot) {
        locked[slot] = !locked[slot];
        saveLockedItems();
    }

    function reroll(slot, save=true) {
        if (locked[slot]) return;
        selected[slot] = pickRandom(available[slot.split("_")[0]].filter(p => p.checked));

        if(!save) return;
        saveSelectedItems();
    }

    function rerollAll() {
        Object.keys(selected).forEach(p => reroll(p, false));
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
            {:else if !available[slot.toLowerCase().split("_")[0]]?.filter(p => p.checked).length}
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
    <div class="grid grid-cols-3 gap-6 mb-10">
        {#each ['primary', 'secondary', 'grenade'] as slot}
            {@render WeaponContainer(slot)}
        {/each}
    </div>

    <div class="grid grid-cols-5 gap-4 mb-10">
        <div class="col-span-4 border rounded-lg p-4 relative">
            {@render ContainerHeader("Stratagem", "Stratagems")}
            <div class="grid grid-cols-4 gap-4">
                {#each ['stratagem_0', 'stratagem_1', 'stratagem_2', 'stratagem_3'] as slot}
                    {@render WeaponContainer(slot, false)}
                {/each}
            </div>
        </div>

        {@render WeaponContainer("booster")}
    </div>

    <div class="flex justify-center gap-10">
        <button class="bg-blue-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onclick={rerollAll}>
            <IconDice class="inline-block mr-1 text-2xl" /> Reroll All
        </button>
        <a class="bg-green-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-green-700 transition cursor-pointer" href="/warbonds">
            <IconList class="inline-block mr-1 text-2xl" /> Select available items
        </a>
    </div>
</div>

<style>
    img {
        max-width: 100%;
        height: auto;
    }
</style>