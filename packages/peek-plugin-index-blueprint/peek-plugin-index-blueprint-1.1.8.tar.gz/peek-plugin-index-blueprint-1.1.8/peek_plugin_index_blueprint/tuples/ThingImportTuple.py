import json
from typing import Dict

from vortex.Tuple import addTupleType, TupleField, Tuple

from peek_plugin_index_blueprint._private.PluginNames import indexBlueprintTuplePrefix


@addTupleType
class ThingImportTuple(Tuple):
    """ Import ThingIndex Tuple

    This tuple is the publicly exposed ThingIndex

    """
    __tupleType__ = indexBlueprintTuplePrefix + 'ThingImportTuple'

    #:  The unique key of this thingIndex
    key: str = TupleField()

    #:  The model set of this thingIndex
    modelSetKey: str = TupleField()

    #:  The thingIndex type
    thingTypeKey: str = TupleField()

    #:  The hash of this import group
    importGroupHash: str = TupleField()

    #:  A string value of the thing
    valueStr: str = TupleField()

    #:  An int value of the thing
    valueInt: int = TupleField()

    # Add more values here

    def packJson(self, modelSetId: int, thingTypeId: int) -> str:
        """ Pack JSON

        This is used by the import worker to pack this object into the index.

        """
        packedJsonDict = dict(
            _msid=modelSetId,
            _tid=thingTypeId
        )

        # Pack the custom data here
        packedJsonDict["valueStr"] = self.valueStr
        packedJsonDict["valueInt"] = self.valueInt

        return json.dumps(packedJsonDict, sort_keys=True)
