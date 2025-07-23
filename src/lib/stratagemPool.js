import _ from "lodash";
import { pickRandom } from "./constants";

export default class StratagemPool{

    constructor(pool, groups){
        this.pool = pool;
        this.groups = groups
            .filter(p => p.enabled)
            .map(p => ({
                ...p,
                picked: 0
            }));
    }

    remove(item){
        this.pool = this.pool.filter(p => p.id != item.id);
    }

    removeAll(items){
        const idsToRemove = new Set(items.map(p => p.id))
        this.pool = this.pool.filter(p => !idsToRemove.has(p.id));
    }

    /** Picks the next available stratagem randomly.
     * If there is one or more groups with a min-value greater than zero,
     * where not enough items have been picked yet, the stratagem will be
     * picked from a random one of these groups.
     * Otherwise, the stratagem will be picked at random from the entire
     * available pool.
     */
    pickNext(){
        const groupsInNeedOfPicks = this.groups.filter(p => p.min > 0 && p.picked < p.min);
        if(groupsInNeedOfPicks.length > 0){
            const items = _(groupsInNeedOfPicks).map("items").flatten().value();
            console.log("Picking from " + groupsInNeedOfPicks.length + " groups in need of picks, with " + items.length + " items (full pool has " + this.pool.length + ").");
            const picked = pickRandom(items);
            return this.picked(picked);
        }

        console.log("Picking from full pool of " + this.pool.length + " items");
        return this.picked(pickRandom(this.pool));
    }

    /** Removes the picked item from the available pool, and checks
     * if the number of items picked from a group exceeds the configured
     * maximum number. If so, removes all items from this group from the pool.
     */
    picked(item){

        if(!item) return item;

        console.log("Removing picked item " + item.name);

        this.remove(item);

        for(const gs of this.groups){
            if(gs.items.some(p => p.id == item.id)){
                console.log("  > Also removed from group " + gs.title);
                gs.items = gs.items.filter(p => p.id != item.id);
                gs.picked++;
                if(gs.picked >= gs.max){
                    this.removeAll(gs.items);
                    console.log("    > Which is now full (" + gs.max + "), removed " + gs.items.length + " items, new pool: " + this.pool.length);
                }
            }
        }

        return item;
    }

}