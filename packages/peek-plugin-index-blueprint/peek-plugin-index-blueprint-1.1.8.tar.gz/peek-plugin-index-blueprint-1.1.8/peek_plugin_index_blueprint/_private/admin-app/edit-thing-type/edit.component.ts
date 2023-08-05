import {Component, OnInit} from "@angular/core";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {
    ComponentLifecycleEventEmitter,
    extend,
    TupleDataObserverService,
    TupleLoader,
    TupleSelector,
    VortexService
} from "@synerty/vortexjs";
import {indexBlueprintFilt} from "@peek/peek_plugin_index_blueprint/_private";
import {ThingTypeTuple, IndexBlueprintModelSetTuple} from "@peek/peek_plugin_index_blueprint";


@Component({
    selector: 'pl-index-blueprint-edit-thing-type',
    templateUrl: './edit.component.html'
})
export class EditThingTypeComponent extends ComponentLifecycleEventEmitter {
    // This must match the dict defined in the admin_backend handler
    private readonly filt = {
        "key": "admin.Edit.ThingType"
    };

    items: ThingTypeTuple[] = [];

    loader: TupleLoader;
    modelSetById: { [id: number]: IndexBlueprintModelSetTuple } = {};
    thingTypeById: { [id: number]: ThingTypeTuple } = {};

    constructor(private balloonMsg: Ng2BalloonMsgService,
                vortexService: VortexService,
                private tupleObserver: TupleDataObserverService) {
        super();

        this.loader = vortexService.createTupleLoader(
            this, () => extend({}, this.filt, indexBlueprintFilt)
        );

        this.loader.observable
            .subscribe((tuples: ThingTypeTuple[]) => this.items = tuples);

        // let modelSetTs = new TupleSelector(ModelSetTuple.tupleName, {});
        // this.tupleObserver.subscribeToTupleSelector(modelSetTs)
        //     .takeUntil(this.onDestroyEvent)
        //     .subscribe((tuples: ModelSetTuple[]) => {
        //         this.modelSetById = {};
        //         for (let tuple of tuples) {
        //             this.modelSetById[tuple.id] = tuple;
        //         }
        //     });
        //
        // let thingTypeTs = new TupleSelector(ThingType.tupleName, {});
        // this.tupleObserver.subscribeToTupleSelector(thingTypeTs)
        //     .takeUntil(this.onDestroyEvent)
        //     .subscribe((tuples: ThingType[]) => {
        //         this.thingTypeById = {};
        //         for (let tuple of tuples) {
        //             this.thingTypeById[tuple.id] = tuple;
        //         }
        //     });
    }

    modelSetTitle(tuple: ThingTypeTuple): string {
        // let modelSet = this.modelSetById[tuple.modelSetId];
        // return modelSet == null ? "" : modelSet.name;
        return "TODO";
    }

    thingTypeTitle(tuple: ThingTypeTuple): string {
        // let thingType = this.thingTypeById[tuple.thing];
        // return thingType == null ? "" : thingType.name;
        return "TODO";
    }

    save() {
        this.loader.save()
            .then(() => this.balloonMsg.showSuccess("Save Successful"))
            .catch(e => this.balloonMsg.showError(e));
    }

    resetClicked() {
        this.loader.load()
            .then(() => this.balloonMsg.showSuccess("Reset Successful"))
            .catch(e => this.balloonMsg.showError(e));
    }


}