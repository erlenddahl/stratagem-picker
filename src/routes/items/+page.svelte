<script>
    import _ from "lodash";
    import IconBack from 'virtual:icons/ion/arrow-back-circle';
    import IconChevron from 'virtual:icons/ion/chevron-forward';
    
    import IconChecked from 'virtual:icons/fluent/checkbox-checked-24-filled';
    import IconIndeterminate from 'virtual:icons/fluent/checkbox-indeterminate-24-filled';
    import IconUnchecked from 'virtual:icons/fluent/checkbox-unchecked-24-filled';
    import ItemTile from '$lib/ItemTile.svelte';

	import { setCookie } from "$lib/constants.js";

    let { data } = $props();

    const warbondSortOrder = [
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
        "Control Group",
        "Halo: ODST",
        "Dust Devils",
        "Python Commandos",
        "Righteous Revenants",
        "Redacted Regiment",
        "Siege Breakers",
        "Entrenched Division",
        "Exo Experts",
        "Castellan's Creed",
        "Ironclad Democracy"
    ];

    function saveCheckedWeapons() {
        const checkedIds = _(warbonds)
            .map("items")
            .flatten()
            .filter(w => w.checked)
            .map(w => w.id)
            .value();
        setCookie("checkedWeapons", checkedIds);
    }

    $effect(() => saveCheckedWeapons(warbonds));

    function createWarbondData(weapons){
        return _(weapons)
            .filter(p => !p.disabled)
            .groupBy('warbond')
            .map((items, warbond) => ({
                title: warbond,
                sortIndex: warbondSortOrder.indexOf(warbond),
                items
            }))
            .sortBy("sortIndex")
            .value();
    }

    let warbonds = $state(createWarbondData(data.weapons));
    
    function toggleAll(items, value=undefined){
        const newValue = value==undefined ? !items[0].checked : value;
        for(const item of items){
            item.checked = newValue
        }
    }

    function getGroupStatus(items) {
        const allChecked = _.every(items, 'checked');
        const noneChecked = _.every(items, item => !item.checked);

        if (allChecked) {
            return 'all';
        } else if (noneChecked) {
            return 'none';
        } else {
            return 'some';
        }
    }

    function getGroupColors(items) {
        const status = getGroupStatus(items);

        if (status == "all") {
            return 'text-green-400';
        } else if (status == "none") {
            return 'text-gray-400';
        } else {
            return 'text-yellow-400';
        }
    }

    function selectAll(value){
        for(const warbond of warbonds){
            toggleAll(warbond.items, value);
        }
    }

    function openAll(value){
        for(const warbond of warbonds){
            warbond.opened = value;
        }
    }

</script>

<div class="m-10">

    <a class="bg-blue-600 text-white font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-blue-700 transition cursor-pointer" href="/">
        <IconBack class="inline-block mr-1 text-2xl" />  Back to stratagem picker
    </a>

    <p class="mb-5">Here you can filter which items you want to be pickable. Tap a section header to open it and see the individual items, or tap the checkbox to toggle all items in this section on or off at the same time.</p>

    <p class="mb-5">The items you have selected will be stored in this browser, so that you can re-use the same selection the next time you open the page in the same browser.</p>

    <div class="flex flex-row gap-5 mb-5">
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => selectAll(true)} data-umami-event="select-all">
            <IconChecked class="inline-block mr-1 text-2xl" />  Select all
        </button>
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => selectAll(false)} data-umami-event="select-none">
            <IconUnchecked class="inline-block mr-1 text-2xl" />  Select none
        </button>
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => openAll(true)} data-umami-event="open-all">
            <IconChevron class="inline-block mr-1 text-2xl rotate-90" />  Open all
        </button>
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => openAll(false)} data-umami-event="close-all">
            <IconChevron class="inline-block mr-1 text-2xl" />  Close all
        </button>
    </div>

    {#each warbonds as warbond}
        {@const status = getGroupStatus(warbond.items)}
        <div class="flex flex-row gap-3 border-b-gray-400 pb-3" class:border-b={warbond.opened}>
            <button class="{getGroupColors(warbond.items)} cursor-pointer rounded-md font-bold w-8 h-8 shrink-0 flex flex-col justify-center items-center text-2xl leading-none" onclick={() => toggleAll(warbond.items)}>
                {#if status == "all"}
                    <IconChecked />
                {:else if status == "none"}
                    <IconUnchecked />
                {:else}
                    <IconIndeterminate />
                {/if}
            </button>
            <button class="cursor-pointer flex min-w-0 flex-1 flex-row gap-5 text-left" onclick={() => warbond.opened = !warbond.opened}>
                <div class="rounded-md font-bold w-8 h-8 shrink-0 flex flex-col justify-center items-center text-2xl leading-none" class:rotate-90={warbond.opened}>
                    <IconChevron />
                </div>
                <span class="min-w-0 text-left text-2xl font-bold wrap-anywhere">{warbond.title}</span>
            </button>
            <button class="cursor-pointer shrink-0 whitespace-nowrap" onclick={() => toggleAll(warbond.items)}>[{warbond.items.filter(p => p.checked).length} / {warbond.items.length}]</button>
        </div>
        {#if warbond.opened}
            <div class="flex flex-wrap mb-10">
                {#each warbond.items as weapon}
                    <ItemTile item={weapon} onToggle={() => weapon.checked = !weapon.checked} />
                {/each}
            </div>
        {/if}
    {/each}
</div>
