<script>
    import IconChecked from 'virtual:icons/fluent/checkbox-checked-24-filled';

    let { item, onToggle } = $props();

    function getScale(item) {
        if (item.category === 'Stratagem') return 0.25;
        if (item.category === 'Booster') return 0.30;
        return 0.45;
    }
</script>

{#snippet contents()}
    <div class="inline-block">
        <img
            src={item.icon_file}
            alt=""
            style="max-width: {249 * getScale(item)}px; max-height: {180 * getScale(item)}px"
            class="m-5 transition-opacity duration-300 {onToggle && !item.checked ? 'opacity-50 grayscale' : 'opacity-100'}"
        />
    </div>
    <p class="truncate">{item.name}</p>
    {#if onToggle && item.checked}
        <div class="absolute bottom-3 left-1 text-green-400 rounded-md font-bold w-8 h-8 flex flex-col justify-center items-center text-2xl leading-none">
            <IconChecked />
        </div>
    {/if}
{/snippet}

<div class="relative m-5 w-96 h-24">
    {#if onToggle}
        <button type="button" class="flex flex-row items-center justify-start gap-5 rounded-md border border-gray-400 hover:bg-gray-300 p-5 cursor-pointer w-full h-full" onclick={onToggle} aria-label={`${item.checked ? 'Disable' : 'Enable'} ${item.name}`}>
            {@render contents()}
        </button>
    {:else}
        <div class="flex flex-row items-center justify-start gap-5 rounded-md border border-gray-400 p-5 w-full h-full">
            {@render contents()}
        </div>
    {/if}
    <a href={item.url} target="_blank" rel="noopener noreferrer" aria-label={`More information about ${item.name}`} class="absolute top-1 right-1 bg-blue-200 text-blue-400 opacity-25 hover:opacity-100 rounded-md font-bold w-5 h-5 flex flex-col justify-center items-center text-sm leading-none">i</a>
</div>
