<script>
    import IconChecked from 'virtual:icons/ion/checkbox-outline';
    import IconUnchecked from 'virtual:icons/ion/square-outline';
    import RangeSlider from 'svelte-range-slider-pips'

    let { title, enabled, items, min, max, id, onchange } = $props();

    function validate(num, fallback){
        if(num == 0 || num == 1 || num == 2 || num == 3 || num == 4) return num;
        return fallback;
    }

    let values = $state([validate(min, 0), validate(max, 4)]);

    const sendOnChange = () => onchange(id, enabled, values[0], values[1]);

    const toggle = () => {
        enabled = !enabled;
        sendOnChange();
    }
</script>

<div class="p-4 border rounded shadow">
    <button class="w-full flex items-center justify-between cursor-pointer" onclick={toggle} data-umami-event="toggle-rule-{id}">
        <div class="flex flex-col items-start">
            <span class="text-lg font-semibold">{title}</span>
            <div class="flex flex-row gap-1">
                {#each items as item}
                    <img src={item.icon_file} alt={item.name} title={item.name} class="max-h-8 {item.checked ? "" : "opacity-50 grayscale"}" />
                {/each}
            </div>
        </div>
        <div>
            {#if enabled}
                <IconChecked class="text-2xl" />
            {:else}
                <IconUnchecked class="text-2xl" />
            {/if}
        </div>
    </button>
  
    {#if enabled}
        <div class="mt-6">
            <RangeSlider bind:values min={0} max={4} on:change={sendOnChange} range pushy pips />
        </div>
        <div>
            {#if values[0] == values[1]}
                Pick exactly {values[0]} items from this group.
            {:else}
                Pick at least {values[0]} items from this group, but not more than {values[1]}.
            {/if}
        </div>
    {/if}
</div>