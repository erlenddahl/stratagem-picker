<script>
    import IconBack from 'virtual:icons/ion/arrow-back-circle';
    import ItemTile from '$lib/ItemTile.svelte';

    let { data } = $props();
    const entries = data.changelog;
    const itemsById = new Map(data.weapons.map((item) => [item.id, item]));

    function dateLabel(date) {
        return new Intl.DateTimeFormat('en-GB', {
            day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC'
        }).format(new Date(`${date}T00:00:00Z`));
    }
</script>

<div class="m-10">
    <a class="bg-blue-600 text-white font-bold px-6 py-3 inline-block mb-5 rounded-lg hover:bg-blue-700 transition cursor-pointer" href="/">
        <IconBack class="inline-block mr-1 text-2xl" /> Back to stratagem picker
    </a>

    <h1 class="text-3xl font-bold mb-8">Changelog</h1>

    {#each entries as entry}
        <section class="mb-8">
            <div class="flex items-center gap-3 border-b border-gray-400 pb-3">
                <time datetime={entry.date} class="text-2xl font-bold">{dateLabel(entry.date)}</time>
                <span class="text-gray-500">({entry.itemIds.length} items)</span>
            </div>
            <p class="mt-3 ml-5">
                <strong>Added warbonds:</strong> {entry.warbonds.length ? entry.warbonds.join(', ') : 'None'}
            </p>
            <div class="flex flex-wrap">
                {#each entry.itemIds as id}
                    {@const item = itemsById.get(id)}
                    {#if item}
                        <ItemTile {item} />
                    {/if}
                {/each}
            </div>
        </section>
    {/each}
</div>
