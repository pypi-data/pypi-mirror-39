import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "../PluginNames";


@addTupleType
export class ThingIndexEncodedChunkTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ThingIndexEncodedChunkTuple";

    chunkKey: string;
    lastUpdate: string;
    encodedData: string;

    constructor() {
        super(ThingIndexEncodedChunkTuple.tupleName)
    }
}
