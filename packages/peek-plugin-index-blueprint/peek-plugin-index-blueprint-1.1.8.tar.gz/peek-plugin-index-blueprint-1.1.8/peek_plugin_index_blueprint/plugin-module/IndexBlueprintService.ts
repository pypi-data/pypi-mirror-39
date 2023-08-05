import {Injectable} from "@angular/core";

import {
    ComponentLifecycleEventEmitter,
    Payload,
    TupleActionPushService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleSelector,
    VortexStatusService
} from "@synerty/vortexjs";

import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import {ThingIndexResultI, ThingIndexLoaderService} from "./_private/thing-index-loader";

// ----------------------------------------------------------------------------
/** ThingIndex Cache
 *
 * This class has the following responsibilities:
 *
 * 1) Maintain a local storage of the index
 *
 * 2) Return DispKey locations based on the index.
 *
 */
@Injectable()
export class IndexBlueprintService extends ComponentLifecycleEventEmitter {


    constructor(private thingIndexLoader: ThingIndexLoaderService) {
        super();

    }

    /** Get Things
     *
     * Get the objects for key from the index..
     *
     */
    getThings(modelSetKey: string, keys: string[]): Promise<ThingIndexResultI> {
        return this.thingIndexLoader.getThings(modelSetKey, keys);
    }

}