import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "../PluginNames";


@addTupleType
export class ThingIndexUpdateDateTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ThingIndexUpdateDateTuple";

    // Improve performance of the JSON serialisation
    protected _rawJonableFields = ['initialLoadComplete', 'updateDateByChunkKey'];

    initialLoadComplete: boolean = false;
    updateDateByChunkKey: {} = {};

    constructor() {
        super(ThingIndexUpdateDateTuple.tupleName)
    }
}