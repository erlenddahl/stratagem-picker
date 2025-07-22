<script>
    import _ from "lodash";
    import IconBack from 'virtual:icons/ion/arrow-back-circle';
    import IconChecked from 'virtual:icons/ion/checkbox-outline';
    import IconUnchecked from 'virtual:icons/ion/square-outline';
	import RangeSelector from "./RangeSelector.svelte";
	import { setCookie } from "$lib/constants";

    let { data } = $props();

    function onchange(id, enabled, min, max){
        const g = data.groups[id];
        g.enabled = enabled;
        g.min = min;
        g.max = max;

        const cookieData = _(data.groups)
            .values()
            .map(p => ({id: p.id, enabled: p.enabled, min: p.min, max: p.max}))
            .value();

        setCookie("groups", cookieData);
    }

</script>

<div class="m-10">

    <a class="bg-blue-600 text-white font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-blue-700 transition cursor-pointer" href="/">
        <IconBack class="inline-block mr-1 text-2xl" />  Back to stratagem picker
    </a>

    <p class="mb-5">These are options.</p>

    <p class="mb-5">The options you have selected will be stored in this browser, so that you can re-use the same options the next time you open the page in the same browser.</p>

    <div class="flex flex-col gap-5">
        {#each Object.values(data.groups) as g}
            <RangeSelector {...g} {onchange} />
        {/each}
    </div>

</div>