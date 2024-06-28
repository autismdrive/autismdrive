import {enableProdMode, importProvidersFrom} from '@angular/core';
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';
import {AppComponent} from '@app/app.component';
import {AppModule} from '@app/app.module';
import {environment} from '@environments/environment';
import {bootstrapApplication} from '@node_modules/@angular/platform-browser';

if (environment.production) {
  enableProdMode();
}

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .catch(err => console.error(err));

bootstrapApplication(AppComponent, {providers: [importProvidersFrom(AppModule)]});
