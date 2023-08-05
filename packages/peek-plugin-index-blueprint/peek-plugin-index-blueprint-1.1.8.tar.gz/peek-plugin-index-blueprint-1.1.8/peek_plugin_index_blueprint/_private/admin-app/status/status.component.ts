import {Component} from "@angular/core";
import {
    ComponentLifecycleEventEmitter,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";
import {ThingIndexServerStatusTuple, indexBlueprintFilt} from "@peek/peek_plugin_index_blueprint/_private";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";


@Component({
    selector: 'pl-index-blueprint-status',
    templateUrl: './status.component.html'
})
export class StatusComponent extends ComponentLifecycleEventEmitter {

    item: ThingIndexServerStatusTuple = new ThingIndexServerStatusTuple();

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private tupleObserver: TupleDataObserverService) {
        super();

        let ts = new TupleSelector(ThingIndexServerStatusTuple.tupleName, {});
        this.tupleObserver.subscribeToTupleSelector(ts)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: ThingIndexServerStatusTuple[]) => {
                this.item = tuples[0];
            });

    }


}