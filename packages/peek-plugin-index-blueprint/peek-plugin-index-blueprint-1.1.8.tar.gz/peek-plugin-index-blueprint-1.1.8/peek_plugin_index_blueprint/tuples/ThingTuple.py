import json
from typing import Dict

from vortex.Tuple import Tuple, addTupleType, TupleField

from peek_plugin_index_blueprint._private.PluginNames import indexBlueprintTuplePrefix
from peek_plugin_index_blueprint._private.storage.ModelSet import \
    ModelSet
from peek_plugin_index_blueprint._private.storage.ThingType import \
    ThingType
from peek_plugin_index_blueprint.tuples.IndexBlueprintModelSetTuple import \
    IndexBlueprintModelSetTuple
from peek_plugin_index_blueprint.tuples.ThingTypeTuple import ThingTypeTuple


@addTupleType
class ThingTuple(Tuple):
    """ ThingIndex Tuple

    This tuple is the publicly exposed ThingIndex

    """
    __tupleType__ = indexBlueprintTuplePrefix + 'ThingTuple'

    #:  The unique key of this thingIndex
    key: str = TupleField()

    #:  The model set of this thingIndex
    modelSet: IndexBlueprintModelSetTuple = TupleField()

    #:  The thingIndex type
    thingType: ThingTypeTuple = TupleField()

    #:  A string value of the thing
    valueStr: str = TupleField()

    #:  An int value of the thing
    valueInt: int = TupleField()

    # Add more values here

    @classmethod
    def unpackJson(self, key: str, packedJson: str):
        # Reconstruct the data
        objectProps: {} = json.loads(packedJson)

        # Get out the object type
        thisThingTypeId = objectProps['_tid']

        # Get out the object type
        thisModelSetId = objectProps['_msid']

        # Create the new object
        newSelf = ThingTuple()

        newSelf.key = key

        # These objects get replaced with the full object in the UI
        newSelf.modelSet = IndexBlueprintModelSetTuple(id__=thisModelSetId)
        newSelf.thingType = ThingTypeTuple(id__=thisThingTypeId)

        # Unpack the custom data here
        newSelf.valueStr = objectProps.get('valueStr')
        newSelf.valueInt = objectProps.get('valueInt')

        return newSelf
