import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {RouterModule, Routes} from "@angular/router";
import {StatusComponent} from "./status/status.component";
// Import our components
import {ThingIndexComponent} from "./index-blueprint.component";
import {
    TupleActionPushNameService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";

import {
    indexBlueprintActionProcessorName,
    indexBlueprintFilt,
    indexBlueprintObservableName,
    indexBlueprintTupleOfflineServiceName
} from "@peek/peek_plugin_index_blueprint/_private";
import {EditThingTypeComponent} from "./edit-thing-type/edit.component";


export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        indexBlueprintActionProcessorName, indexBlueprintFilt);
}

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        indexBlueprintObservableName, indexBlueprintFilt);
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService(indexBlueprintTupleOfflineServiceName);
}

// Define the routes for this Angular module
export const pluginRoutes: Routes = [
    {
        path: '',
        component: ThingIndexComponent
    }

];

// Define the module
@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(pluginRoutes),
        FormsModule
    ],
    exports: [],
    providers: [
        TupleActionPushService, {
            provide: TupleActionPushNameService,
            useFactory: tupleActionPushNameServiceFactory
        },
        TupleOfflineStorageService, {
            provide: TupleOfflineStorageNameService,
            useFactory: tupleOfflineStorageNameServiceFactory
        },
        TupleDataObserverService, TupleDataOfflineObserverService, {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        },
    ],
    declarations: [ThingIndexComponent,
        StatusComponent,
        EditThingTypeComponent]
})
export class ThingIndexModule {

}
