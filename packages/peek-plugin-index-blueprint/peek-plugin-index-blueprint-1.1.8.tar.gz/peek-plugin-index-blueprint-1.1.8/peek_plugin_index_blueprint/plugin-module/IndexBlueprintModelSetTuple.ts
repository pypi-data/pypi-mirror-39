import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "./_private/PluginNames";


@addTupleType
export class IndexBlueprintModelSetTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ModelSetTuple";

    //  A protected variable
    id__: number;

    //  The unique key of this ModelSet
    key: string;

    //  The unique name of this ModelSet
    name: string;

    constructor() {
        super(IndexBlueprintModelSetTuple.tupleName)
    }

}