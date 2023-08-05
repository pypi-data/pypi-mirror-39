import {BrowserModule} from "@angular/platform-browser";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {NgModule} from "@angular/core";
import {FormsModule} from "@angular/forms";
import {HttpModule} from "@angular/http";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {Ng2BalloonMsgModule} from "@synerty/ng2-balloon-msg-web";
import {
    TupleStorageFactoryService,
    VortexService,
    VortexStatusService,
    WebSqlFactoryService
} from "@synerty/vortexjs";

import {
    TupleStorageFactoryServiceWeb,
    WebSqlBrowserFactoryService
} from "@synerty/vortexjs/index-browser";
import {AppRoutingModule} from "./app/app-routing.module";
import {AppComponent} from "./app/app.component";
import {DashboardModule} from "./app/dashboard/dashboard.module";
import {SettingModule} from "./app/setting/setting.module";
import {NavbarModule} from "./app/navbar/navbar.module";
import {UpdateModule} from "./app/update/update.module";

import {AngularFontAwesomeModule} from "angular-font-awesome/dist/angular-font-awesome";

import {ACE_CONFIG, AceConfigInterface, AceModule} from 'ngx-ace-wrapper';

const DEFAULT_ACE_CONFIG: AceConfigInterface = {};

@NgModule({
    declarations: [
        AppComponent,
    ],
    imports: [
        AceModule,
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        AngularFontAwesomeModule,
        HttpModule,
        AppRoutingModule,
        Ng2BalloonMsgModule,
        DashboardModule,
        SettingModule,
        NavbarModule,
        UpdateModule
    ],
    providers: [
        {
            provide: ACE_CONFIG,
            useValue: DEFAULT_ACE_CONFIG
        },
        {provide: WebSqlFactoryService, useClass: WebSqlBrowserFactoryService},
        {provide: TupleStorageFactoryService, useClass: TupleStorageFactoryServiceWeb},
        Ng2BalloonMsgService, VortexService, VortexStatusService],
    bootstrap: [AppComponent]
})
export class AppModule {

}
