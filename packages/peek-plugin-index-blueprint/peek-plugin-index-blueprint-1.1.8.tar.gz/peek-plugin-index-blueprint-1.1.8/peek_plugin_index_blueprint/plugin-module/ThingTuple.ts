import {addTupleType, Tuple} from "@synerty/vortexjs";
import {indexBlueprintTuplePrefix} from "./_private/PluginNames";
import {ThingTypeTuple} from "./ThingTypeTuple";
import {IndexBlueprintModelSetTuple} from "./IndexBlueprintModelSetTuple";


@addTupleType
export class ThingTuple extends Tuple {
    public static readonly tupleName = indexBlueprintTuplePrefix + "ThingTuple";

    //  The unique key of this thingIndex
    key: string;

    //  The modelSetId for this thingIndex.
    modelSet: IndexBlueprintModelSetTuple = new IndexBlueprintModelSetTuple();

    // This ThingIndex Type ID
    thingType: ThingTypeTuple = new ThingTypeTuple();

    // A string value of the thing
    valueStr: string;

    // An int value of the thing
    valueInt: number;

    // Add more values here

    constructor() {
        super(ThingTuple.tupleName)
    }

    static unpackJson(key: string, packedJson: string): ThingTuple {
        // Reconstruct the data
        let objectProps: {} = JSON.parse(packedJson);

        // Get out the object type
        let thisThingTypeId = objectProps['_tid'];
        delete objectProps['_tid'];

        // Get out the object type
        let thisModelSetId = objectProps['_msid'];
        delete objectProps['_msid'];

        // Create the new object
        let newSelf = new ThingTuple();

        newSelf.key = key;

        // These objects get replaced later in the UI
        newSelf.modelSet = new IndexBlueprintModelSetTuple();
        newSelf.modelSet.id__ = thisModelSetId;
        newSelf.thingType = new ThingTypeTuple();
        newSelf.thingType.id__ = thisThingTypeId;

        // Unpack the custom data here
        newSelf.valueStr = objectProps["valueStr"];
        newSelf.valueInt = objectProps["valueInt"];

        return newSelf;

    }
}