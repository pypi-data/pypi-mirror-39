import {Component, Input} from "@angular/core";

import {ComponentLifecycleEventEmitter, TupleSelector} from "@synerty/vortexjs";
import {IndexBlueprintTupleService, OfflineConfigTuple} from "@peek/peek_plugin_index_blueprint/_private";
import {
    ThingIndexLoaderService,
    ThingIndexLoaderStatusTuple
} from "@peek/peek_plugin_index_blueprint/_private/thing-index-loader";


@Component({
    selector: 'peek-plugin-index-blueprint-cfg',
    templateUrl: 'index-blueprint-cfg.component.web.html',
    moduleId: module.id
})
export class ThingIndexCfgComponent extends ComponentLifecycleEventEmitter {

    thingIndexStatus: ThingIndexLoaderStatusTuple = new ThingIndexLoaderStatusTuple();

    offlineConfig: OfflineConfigTuple = new OfflineConfigTuple();

    private offlineTs = new TupleSelector(OfflineConfigTuple.tupleName, {});

    constructor(private thingIndexLoader: ThingIndexLoaderService,
                private tupleService: IndexBlueprintTupleService) {
        super();

        this.thingIndexStatus = this.thingIndexLoader.status();
        this.thingIndexLoader.statusObservable()
            .takeUntil(this.onDestroyEvent)
            .subscribe(value => this.thingIndexStatus = value);

        this.tupleService.offlineObserver
            .subscribeToTupleSelector(this.offlineTs, false, false, true)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: OfflineConfigTuple[]) => {
                if (tuples.length == 0) {
                    this.tupleService.offlineObserver
                        .updateOfflineState(this.offlineTs, [this.offlineConfig]);
                    return;
                }
            });

    }

    toggleOfflineMode(): void {
        this.offlineConfig.cacheChunksForOffline = !this.offlineConfig.cacheChunksForOffline;
        this.tupleService.offlineObserver
            .updateOfflineState(this.offlineTs, [this.offlineConfig]);
    }

}
