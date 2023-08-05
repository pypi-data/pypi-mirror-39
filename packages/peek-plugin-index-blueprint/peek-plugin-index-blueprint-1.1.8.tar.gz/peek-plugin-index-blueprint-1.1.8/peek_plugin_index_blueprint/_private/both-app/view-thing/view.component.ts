import {Component, Input, OnInit} from "@angular/core";
import {ActivatedRoute, Params} from "@angular/router";
import {indexBlueprintBaseUrl} from "@peek/peek_plugin_index_blueprint/_private";
import {TitleService} from "@synerty/peek-util";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleSelector,
    VortexStatusService
} from "@synerty/vortexjs";

import {
    IndexBlueprintService,
    ThingIndexResultI,
    ThingTuple,
    ThingTypeTuple
} from "@peek/peek_plugin_index_blueprint";
import {Observable} from "rxjs/Observable";
import {extend} from "@synerty/vortexjs/src/vortex/UtilMisc";


@Component({
    selector: 'plugin-index-blueprint-result',
    templateUrl: 'view.component.web.html',
    moduleId: module.id
})
export class ViewThingComponent extends ComponentLifecycleEventEmitter implements OnInit {

    thing: ThingTuple = null;
    thingTypeName: string = '';

    modelSetKey: string = '';
    key: string = '';

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private route: ActivatedRoute,
                private indexBlueprintService: IndexBlueprintService,
                private vortexStatus: VortexStatusService,
                private titleService: TitleService) {
        super();

        titleService.setTitle("View Thing");

    }

    ngOnInit() {

        this.route.params
            .takeUntil(this.onDestroyEvent)
            .subscribe((params: Params) => {
                let vars = {};

                if (typeof window !== 'undefined') {
                    window.location.href.replace(
                        /[?&]+([^=&]+)=([^&]*)/gi,
                        (m, key, value) => vars[key] = value
                    );
                }

                this.key = params['key'] || vars['key'];
                this.modelSetKey = params['modelSetKey'] || vars['modelSetKey'];

                if (!(this.modelSetKey && this.modelSetKey.length && this.key && this.key.length))
                    return;

                this.titleService.setTitle(`Loading Thing ${this.key}`);
                this.indexBlueprintService
                    .getThings(this.modelSetKey, [this.key])
                    .then((things: ThingIndexResultI) => {
                        this.loadThing(things[this.key], this.key)
                    })
                    .catch(e => this.balloonMsg.showError(e));

            });

    }

    find(): void {
        if (!(this.modelSetKey && this.modelSetKey.length)) {
            this.balloonMsg.showWarning("Please set modelSetKey");
            return;
        }

        if (!(this.key && this.key.length)) {
            this.balloonMsg.showWarning("Please set key");
            return;
        }

        this.indexBlueprintService
            .getThings(this.modelSetKey, [this.key])
            .then((things: ThingIndexResultI) => {
                this.loadThing(things[this.key], this.key)
            })
            .catch(e => this.balloonMsg.showError(e));
    }

    private loadThing(thing: ThingTuple, key: string) {
        this.thing = thing;
        this.thingTypeName = '';

        if (this.thing == null || this.thing.key == null) {
            this.balloonMsg.showWarning(`Failed to find ${key}`);
            this.titleService.setTitle(`Thing ${key} Not Found`);
            return;
        }
        this.balloonMsg.showSuccess(`We've found ${key}`);

        this.titleService.setTitle(`Thing ${key}`);

        this.thingTypeName = this.thing.thingType.name;
    }


}