import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "./_private/PluginNames";


@addTupleType
export class ThingTypeTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ThingTypeTuple";

    //  A protected variable
    id__: number;

    //  The key of this ThingType
    key: string;

    //  The key of the model set
    modelSetKey: string;

    //  The name of the ThingType
    name: string;

    constructor() {
        super(ThingTypeTuple.tupleName)
    }
}