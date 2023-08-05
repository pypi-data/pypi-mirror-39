import {Injectable} from "@angular/core";

import {
    ComponentLifecycleEventEmitter,
    extend,
    Payload,
    PayloadEnvelope,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    TupleSelector,
    TupleStorageFactoryService,
    VortexService,
    VortexStatusService
} from "@synerty/vortexjs";

import {
    indexBlueprintCacheStorageName,
    indexBlueprintFilt,
    indexBlueprintTuplePrefix
} from "../PluginNames";


import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import {ThingIndexEncodedChunkTuple} from "./ThingIndexEncodedChunkTuple";
import {ThingIndexUpdateDateTuple} from "./ThingIndexUpdateDateTuple";
import {ThingTuple} from "../../ThingTuple";
import {IndexBlueprintTupleService} from "../index-blueprint-tuple.service";
import {ThingTypeTuple} from "../../ThingTypeTuple";
import {ThingIndexLoaderStatusTuple} from "./ThingIndexLoaderStatusTuple";

import {OfflineConfigTuple} from "../tuples/OfflineConfigTuple";
import {IndexBlueprintModelSetTuple} from "../../IndexBlueprintModelSetTuple";

// ----------------------------------------------------------------------------

export interface ThingIndexResultI {
    [key: string]: ThingTuple
}

// ----------------------------------------------------------------------------

let clientThingIndexWatchUpdateFromDeviceFilt = extend(
    {'key': "clientThingIndexWatchUpdateFromDevice"},
    indexBlueprintFilt
);

const cacheAll = "cacheAll";

// ----------------------------------------------------------------------------
/** ThingIndexChunkTupleSelector
 *
 * This is just a short cut for the tuple selector
 */

class ThingIndexChunkTupleSelector extends TupleSelector {

    constructor(private chunkKey: string) {
        super(indexBlueprintTuplePrefix + "ThingIndexChunkTuple", {key: chunkKey});
    }

    toOrderedJsonStr(): string {
        return this.chunkKey;
    }
}

// ----------------------------------------------------------------------------
/** UpdateDateTupleSelector
 *
 * This is just a short cut for the tuple selector
 */
class UpdateDateTupleSelector extends TupleSelector {
    constructor() {
        super(ThingIndexUpdateDateTuple.tupleName, {});
    }
}


// ----------------------------------------------------------------------------
/** hash method
 */
let BUCKET_COUNT = 8192;

function keyChunk(modelSetKey: string, key: string): string {
    /** Object ID Chunk

     This method creates an int from 0 to MAX, representing the hash bucket for this
     object Id.

     This is simple, and provides a reasonable distribution

     @param modelSetKey: The key of the model set that the thingIndexs are in
     @param key: The key of the thingIndex to get the chunk key for

     @return: The bucket / chunkKey where you'll find the object with this ID

     */
    if (key == null || key.length == 0)
        throw new Error("key is None or zero length");

    let bucket = 0;

    for (let i = 0; i < key.length; i++) {
        bucket = ((bucket << 5) - bucket) + key.charCodeAt(i);
        bucket |= 0; // Convert to 32bit integer
    }

    bucket = bucket & (BUCKET_COUNT - 1);

    return `${modelSetKey}.${bucket}`;
}


// ----------------------------------------------------------------------------
/** ThingIndex Cache
 *
 * This class has the following responsibilities:
 *
 * 1) Maintain a local storage of the index
 *
 * 2) Return DispKey index-blueprint based on the index.
 *
 */
@Injectable()
export class ThingIndexLoaderService extends ComponentLifecycleEventEmitter {
    private UPDATE_CHUNK_FETCH_SIZE = 5;
    private OFFLINE_CHECK_PERIOD_MS = 15 * 60 * 1000; // 15 minutes

    private index = new ThingIndexUpdateDateTuple();
    private askServerChunks: ThingIndexUpdateDateTuple[] = [];

    private _hasLoaded = false;

    private _hasLoadedSubject = new Subject<void>();
    private storage: TupleOfflineStorageService;

    private _statusSubject = new Subject<ThingIndexLoaderStatusTuple>();
    private _status = new ThingIndexLoaderStatusTuple();

    private objectTypesByIds: { [id: number]: ThingTypeTuple } = {};
    private _hasDocTypeLoaded = false;

    private modelSetByIds: { [id: number]: IndexBlueprintModelSetTuple } = {};
    private _hasModelSetLoaded = false;

    private offlineConfig: OfflineConfigTuple = new OfflineConfigTuple();


    constructor(private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                storageFactory: TupleStorageFactoryService,
                private tupleService: IndexBlueprintTupleService) {
        super();

        this.tupleService.offlineObserver
            .subscribeToTupleSelector(new TupleSelector(OfflineConfigTuple.tupleName, {}),
                false, false, true)
            .takeUntil(this.onDestroyEvent)
            .filter(v => v.length != 0)
            .subscribe((tuples: OfflineConfigTuple[]) => {
                this.offlineConfig = tuples[0];
                if (this.offlineConfig.cacheChunksForOffline)
                    this.initialLoad();
                this._notifyStatus();
            });

        let objTypeTs = new TupleSelector(ThingTypeTuple.tupleName, {});
        this.tupleService.offlineObserver
            .subscribeToTupleSelector(objTypeTs)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: ThingTypeTuple[]) => {
                this.objectTypesByIds = {};
                for (let item of tuples) {
                    this.objectTypesByIds[item.id__] = item;
                }
                this._hasDocTypeLoaded = true;
                this._notifyReady();
            });

        let modelSetTs = new TupleSelector(IndexBlueprintModelSetTuple.tupleName, {});
        this.tupleService.offlineObserver
            .subscribeToTupleSelector(modelSetTs)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: IndexBlueprintModelSetTuple[]) => {
                this.modelSetByIds = {};
                for (let item of tuples) {
                    this.modelSetByIds[item.id__] = item;
                }
                this._hasModelSetLoaded = true;
                this._notifyReady();
            });

        this.storage = new TupleOfflineStorageService(
            storageFactory,
            new TupleOfflineStorageNameService(indexBlueprintCacheStorageName)
        );

        this.setupVortexSubscriptions();
        this._notifyStatus();

        // Check for updates every so often
        Observable.interval(this.OFFLINE_CHECK_PERIOD_MS)
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this.askServerForUpdates());
    }

    isReady(): boolean {
        return this._hasLoaded;
    }

    isReadyObservable(): Observable<void> {
        return this._hasLoadedSubject;
    }

    statusObservable(): Observable<ThingIndexLoaderStatusTuple> {
        return this._statusSubject;
    }

    status(): ThingIndexLoaderStatusTuple {
        return this._status;
    }

    private _notifyReady(): void {
        if (this._hasDocTypeLoaded && this._hasModelSetLoaded && this._hasLoaded)
            this._hasLoadedSubject.next();
    }

    private _notifyStatus(): void {
        this._status.cacheForOfflineEnabled = this.offlineConfig.cacheChunksForOffline;
        this._status.initialLoadComplete = this.index.initialLoadComplete;

        this._status.loadProgress = Object.keys(this.index.updateDateByChunkKey).length;
        for (let chunk of this.askServerChunks)
            this._status.loadProgress -= Object.keys(chunk.updateDateByChunkKey).length;

        this._statusSubject.next(this._status);
    }

    /** Initial load
     *
     * Load the dates of the index buckets and ask the server if it has any updates.
     */
    private initialLoad(): void {

        this.storage.loadTuples(new UpdateDateTupleSelector())
            .then((tuplesAny: any[]) => {
                let tuples: ThingIndexUpdateDateTuple[] = tuplesAny;
                if (tuples.length != 0) {
                    this.index = tuples[0];

                    if (this.index.initialLoadComplete) {
                        this._hasLoaded = true;
                        this._notifyReady();
                    }

                }

                this.askServerForUpdates();
                this._notifyStatus();
            });

        this._notifyStatus();
    }

    private setupVortexSubscriptions(): void {

        // Services don't have destructors, I'm not sure how to unsubscribe.
        this.vortexService.createEndpointObservable(this, clientThingIndexWatchUpdateFromDeviceFilt)
            .takeUntil(this.onDestroyEvent)
            .subscribe((payloadEnvelope: PayloadEnvelope) => {
                this.processThingIndexsFromServer(payloadEnvelope);
            });

        // If the vortex service comes back online, update the watch grids.
        this.vortexStatusService.isOnline
            .filter(isOnline => isOnline == true)
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this.askServerForUpdates());

    }

    private areWeTalkingToTheServer(): boolean {
        return this.offlineConfig.cacheChunksForOffline
            && this.vortexStatusService.snapshot.isOnline;
    }


    /** Ask Server For Updates
     *
     * Tell the server the state of the chunks in our index and ask if there
     * are updates.
     *
     */
    private askServerForUpdates() {
        if (!this.areWeTalkingToTheServer()) return;

        // If we're still caching, then exit
        if (this.askServerChunks.length != 0) {
            this.askServerForNextUpdateChunk();
            return;
        }

        this.tupleService.observer
            .pollForTuples(new UpdateDateTupleSelector())
            .then((tuplesAny: any) => {
                let serverIndex: ThingIndexUpdateDateTuple = tuplesAny[0];
                let keys = Object.keys(serverIndex.updateDateByChunkKey);
                let keysNeedingUpdate: string[] = [];

                this._status.loadTotal = keys.length;

                // Tuples is an array of strings
                for (let chunkKey of keys) {
                    if (!this.index.updateDateByChunkKey.hasOwnProperty(chunkKey)) {
                        this.index.updateDateByChunkKey[chunkKey] = null;
                        keysNeedingUpdate.push(chunkKey);

                    } else if (this.index.updateDateByChunkKey[chunkKey]
                        != serverIndex.updateDateByChunkKey[chunkKey]) {
                        keysNeedingUpdate.push(chunkKey);
                    }
                }
                this.queueChunksToAskServer(keysNeedingUpdate);
            });
    }


    /** Queue Chunks To Ask Server
     *
     */
    private queueChunksToAskServer(keysNeedingUpdate: string[]) {
        if (!this.areWeTalkingToTheServer()) return;

        this.askServerChunks = [];

        let count = 0;
        let indexChunk = new ThingIndexUpdateDateTuple();

        for (let key of keysNeedingUpdate) {
            indexChunk.updateDateByChunkKey[key] = this.index.updateDateByChunkKey[key];
            count++;

            if (count == this.UPDATE_CHUNK_FETCH_SIZE) {
                this.askServerChunks.push(indexChunk);
                count = 0;
                indexChunk = new ThingIndexUpdateDateTuple();
            }
        }

        if (count)
            this.askServerChunks.push(indexChunk);

        this.askServerForNextUpdateChunk();

        this._status.lastCheck = new Date();
    }

    private askServerForNextUpdateChunk() {
        if (!this.areWeTalkingToTheServer()) return;

        if (this.askServerChunks.length == 0)
            return;

        let indexChunk: ThingIndexUpdateDateTuple = this.askServerChunks.pop();
        let filt = extend({}, clientThingIndexWatchUpdateFromDeviceFilt);
        filt[cacheAll] = true;
        let pl = new Payload(filt, [indexChunk]);
        this.vortexService.sendPayload(pl);

        this._status.lastCheck = new Date();
        this._notifyStatus();
    }


    /** Process ThingIndexes From Server
     *
     * Process the grids the server has sent us.
     */
    private processThingIndexsFromServer(payloadEnvelope: PayloadEnvelope) {

        if (payloadEnvelope.result != null && payloadEnvelope.result != true) {
            console.log(`ERROR: ${payloadEnvelope.result}`);
            return;
        }

        payloadEnvelope
            .decodePayload()
            .then((payload: Payload) => this.storeThingIndexPayload(payload))
            .then(() => {
                if (this.askServerChunks.length == 0) {
                    this.index.initialLoadComplete = true;
                    this._hasLoaded = true;
                    this._hasLoadedSubject.next();

                } else if (payloadEnvelope.filt[cacheAll] == true) {
                    this.askServerForNextUpdateChunk();

                }

            })
            .then(() => this._notifyStatus())
            .catch(e =>
                `ThingIndexCache.processThingIndexsFromServer failed: ${e}`
            );

    }

    private storeThingIndexPayload(payload: Payload) {

        let tuplesToSave: ThingIndexEncodedChunkTuple[] = <ThingIndexEncodedChunkTuple[]>payload.tuples;
        if (tuplesToSave.length == 0)
            return;

        // 2) Store the index
        this.storeThingIndexChunkTuples(tuplesToSave)
            .then(() => {
                // 3) Store the update date

                for (let indexBlueprintIndex of tuplesToSave) {
                    this.index.updateDateByChunkKey[indexBlueprintIndex.chunkKey] = indexBlueprintIndex.lastUpdate;
                }

                return this.storage.saveTuples(
                    new UpdateDateTupleSelector(), [this.index]
                );

            })
            .catch(e => console.log(
                `ThingIndexCache.storeThingIndexPayload: ${e}`));

    }

    /** Store Index Bucket
     * Stores the index bucket in the local db.
     */
    private storeThingIndexChunkTuples(encodedThingIndexChunkTuples: ThingIndexEncodedChunkTuple[]): Promise<void> {
        let retPromise: any;
        retPromise = this.storage.transaction(true)
            .then((tx) => {

                let promises = [];

                for (let encodedThingIndexChunkTuple of encodedThingIndexChunkTuples) {
                    promises.push(
                        tx.saveTuplesEncoded(
                            new ThingIndexChunkTupleSelector(encodedThingIndexChunkTuple.chunkKey),
                            encodedThingIndexChunkTuple.encodedData
                        )
                    );
                }

                return Promise.all(promises)
                    .then(() => tx.close());
            });
        return retPromise;
    }


    /** Get ThingIndexs
     *
     * Get the objects with matching keywords from the index..
     *
     */
    getThings(modelSetKey: string, keys: string[]): Promise<ThingIndexResultI> {
        if (modelSetKey == null || modelSetKey.length == 0) {
            Promise.reject("We've been passed a null/empty modelSetKey");
        }

        if (keys == null || keys.length == 0) {
            Promise.reject("We've been passed a null/empty keys");
        }

        // If there is no offline support, or we're online
        if (!this.offlineConfig.cacheChunksForOffline
            || this.vortexStatusService.snapshot.isOnline) {
            let ts = new TupleSelector(ThingTuple.tupleName, {
                "modelSetKey": modelSetKey,
                "keys": keys
            });

            let isOnlinePromise: any = this.vortexStatusService.snapshot.isOnline ?
                Promise.resolve() :
                this.vortexStatusService.isOnline
                    .filter(online => online)
                    .first()
                    .toPromise();

            return isOnlinePromise
                .then(() => this.tupleService.offlineObserver.pollForTuples(ts, false))
                .then((docs: ThingTuple[]) => this._populateAndIndexObjectTypes(docs));
        }


        // If we do have offline support
        if (this.isReady())
            return this.getThingsWhenReady(modelSetKey, keys)
                .then(docs => this._populateAndIndexObjectTypes(docs));

        return this.isReadyObservable()
            .first()
            .toPromise()
            .then(() => this.getThingsWhenReady(modelSetKey, keys))
            .then(docs => this._populateAndIndexObjectTypes(docs));
    }


    /** Get ThingIndexs When Ready
     *
     * Get the objects with matching keywords from the index..
     *
     */
    private getThingsWhenReady(
        modelSetKey: string, keys: string[]): Promise<ThingTuple[]> {

        let keysByChunkKey: { [key: string]: string[]; } = {};
        let chunkKeys: string[] = [];

        for (let key of keys) {
            let chunkKey: string = keyChunk(modelSetKey, key);
            if (keysByChunkKey[chunkKey] == null)
                keysByChunkKey[chunkKey] = [];
            keysByChunkKey[chunkKey].push(key);
            chunkKeys.push(chunkKey);
        }


        let promises = [];
        for (let chunkKey of chunkKeys) {
            let keysForThisChunk = keysByChunkKey[chunkKey];
            promises.push(
                this.getThingsForKeys(keysForThisChunk, chunkKey)
            );
        }

        return Promise.all(promises)
            .then((promiseResults: ThingTuple[][]) => {
                let objects: ThingTuple[] = [];
                for (let results of  promiseResults) {
                    for (let result of results) {
                        objects.push(result);
                    }
                }
                return objects;
            });
    }


    /** Get ThingIndexs for Object ID
     *
     * Get the objects with matching keywords from the index..
     *
     */
    private getThingsForKeys(keys: string[], chunkKey: string): Promise<ThingTuple[]> {

        if (!this.index.updateDateByChunkKey.hasOwnProperty(chunkKey)) {
            console.log(`ObjectIDs: ${keys} doesn't appear in the index`);
            return Promise.resolve([]);
        }

        let retPromise: any;
        retPromise = this.storage
            .loadTuplesEncoded(new ThingIndexChunkTupleSelector(chunkKey))
            .then((vortexMsg: string) => {
                if (vortexMsg == null) {
                    return [];
                }


                return Payload.fromEncodedPayload(vortexMsg)
                    .then((payload: Payload) => JSON.parse(<any>payload.tuples))
                    .then((chunkData: { [key: number]: string; }) => {

                        let foundThingIndexs: ThingTuple[] = [];

                        for (let key of keys) {
                            // Find the keyword, we're just iterating
                            if (!chunkData.hasOwnProperty(key)) {
                                console.log(
                                    `WARNING: ThingIndex ${key} is missing from index,`
                                    + ` chunkKey ${chunkKey}`
                                );
                                continue;
                            }

                            let packedJson = chunkData[key];
                            foundThingIndexs
                                .push(ThingTuple.unpackJson(key, packedJson));

                        }

                        return foundThingIndexs;

                    });
            });

        return retPromise;

    }

    private _populateAndIndexObjectTypes(results: ThingTuple[]): ThingIndexResultI {

        let objects: { [key: string]: ThingTuple } = {};
        for (let result of results) {
            objects[result.key] = result;
            result.thingType = this.objectTypesByIds[result.thingType.id__];
            result.modelSet = this.modelSetByIds[result.modelSet.id__];
        }
        return objects;
    }


}