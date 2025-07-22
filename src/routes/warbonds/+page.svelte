<script>
    import _ from "lodash";
    import IconBack from 'virtual:icons/ion/arrow-back-circle';
    import IconChevron from 'virtual:icons/ion/chevron-forward';
    import IconChecked from 'virtual:icons/ion/checkbox-outline';
    import IconUnchecked from 'virtual:icons/ion/square-outline';
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
        "Control Group"
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
                title: warbondSortOrder.indexOf(warbond) >= 7 ? "Warbond: " + warbond : warbond,
                sortIndex: warbondSortOrder.indexOf(warbond),
                items
            }))
            .sortBy("sortIndex")
            .value();
    }

    let warbonds = $state(createWarbondData(data.weapons));
    
    function getScale(item){
        if(item.category == "Stratagem") return 0.25;
        if(item.category == "Booster") return 0.30;
        return 0.45;
    }

    function toggleAll(items, value=undefined){
        const newValue = value==undefined ? !items[0].checked : value;
        for(const item of items){
            item.checked = newValue
        }
    }

    function getGroupColors(items) {
        const allChecked = _.every(items, 'checked');
        const noneChecked = _.every(items, item => !item.checked);

        if (allChecked) {
            return 'bg-green-200 text-green-400';
        } else if (noneChecked) {
            return 'bg-gray-200 text-gray-400';
        } else {
            return 'bg-yellow-200 text-yellow-400';
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

    <p class="mb-5">Here you can filter which items you want to be pickable. Tap a section header to open it and see the individual items, or tap the [X / Y] info to the right of the header to toggle all items in this section on or off at the same time.</p>

    <p class="mb-5">The items you have selected will be stored in this browser, so that you can re-use the same selection the next time you open the page in the same browser.</p>

    <div class="flex flex-row gap-5 mb-5">
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => selectAll(true)}>
            <IconChecked class="inline-block mr-1 text-2xl" />  Select all
        </button>
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => selectAll(false)}>
            <IconUnchecked class="inline-block mr-1 text-2xl" />  Select none
        </button>
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => openAll(true)}>
            <IconChevron class="inline-block mr-1 text-2xl rotate-90" />  Open all
        </button>
        <button class="border font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-gray-200 transition cursor-pointer" onclick={() => openAll(false)}>
            <IconChevron class="inline-block mr-1 text-2xl" />  Close all
        </button>
    </div>

    {#each warbonds as warbond}
        <div class="flex flex-row gap-3 border-b-gray-400 pb-3" class:border-b={warbond.opened}>
            <button class="cursor-pointer flex flex-row gap-5" onclick={() => warbond.opened = !warbond.opened}>
                <div class="{getGroupColors(warbond.items)} rounded-md font-bold w-8 h-8 flex flex-col justify-center items-center text-2xl leading-none" class:rotate-90={warbond.opened}>
                    <IconChevron />
                </div>
                <span class="text-2xl font-bold">{warbond.title}</span>
            </button>
            <button class="cursor-pointer" onclick={() => toggleAll(warbond.items)}>[{warbond.items.filter(p => p.checked).length} / {warbond.items.length}]</button>
        </div>
        {#if warbond.opened}
            <div class="flex flex-wrap mb-10">
                {#each warbond.items as weapon}
                    <button class="relative flex flex-row items-center justify-start gap-5 m-5 rounded-md border border-gray-400 hover:bg-gray-300 p-5 cursor-pointer w-96 h-24" onclick={() => weapon.checked = !weapon.checked}>
                        <div class="inline-block">
                            <img
                                src={weapon.icon_file}
                                alt={weapon.name}
                                style="max-width: {249*getScale(weapon)}px; max-height: {180*getScale(weapon)}px"
                                class="m-5 transition-opacity duration-300 {weapon.checked ? 'opacity-100' : 'opacity-50 grayscale'}"
                            />
                        </div>
                        <p class="truncate">{weapon.name}</p>
                        {#if weapon.checked}
                            <div class="absolute bottom-3 left-1 bg-green-200 text-green-400 rounded-md font-bold w-8 h-8 flex flex-col justify-center items-center text-2xl leading-none">✓</div>
                        {/if}
                        <a href={weapon.url} onclick={e => e.cancelBubble()} target="_blank" class="absolute top-1 right-1 bg-blue-200 text-blue-400 opacity-25 hover:opacity-100 rounded-md font-bold w-5 h-5 flex flex-col justify-center items-center text-sm leading-none">i</a>
                    </button>
                {/each}
            </div>
        {/if}
    {/each}
</div>