import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "../PluginNames";


@addTupleType
export class OfflineConfigTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "OfflineConfigTuple";

    cacheChunksForOffline: boolean = false;

    constructor() {
        super(OfflineConfigTuple.tupleName)
    }
}