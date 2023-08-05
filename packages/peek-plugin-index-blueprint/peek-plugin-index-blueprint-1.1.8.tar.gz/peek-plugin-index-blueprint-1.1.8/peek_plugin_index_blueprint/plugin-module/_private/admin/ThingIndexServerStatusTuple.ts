import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "../PluginNames";


@addTupleType
export class ThingIndexServerStatusTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ThingIndexServerStatusTuple";

    thingIndexCompilerQueueStatus: boolean;
    thingIndexCompilerQueueSize: number;
    thingIndexCompilerQueueProcessedTotal: number;
    thingIndexCompilerQueueLastError: string;

    constructor() {
        super(ThingIndexServerStatusTuple.tupleName)
    }
}