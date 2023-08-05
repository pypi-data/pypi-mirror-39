import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "../PluginNames";


@addTupleType
export class ThingIndexLoaderStatusTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ThingIndexLoaderStatusTuple";


    cacheForOfflineEnabled: boolean = false;
    initialLoadComplete: boolean = false;
    loadProgress: number = 0;
    loadTotal: number = 0;
    lastCheck: Date;

    constructor() {
        super(ThingIndexLoaderStatusTuple.tupleName)
    }
}
