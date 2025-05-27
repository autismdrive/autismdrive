import {ApplicationConfig, importProvidersFrom, mergeApplicationConfig} from '@angular/core';
import {provideServerRendering} from '@angular/platform-server';
import {provideServerRouting} from '@angular/ssr';
import {FlexLayoutServerModule} from '@ngbracket/ngx-layout/server';
import {appConfig} from './app.config';
import {serverRoutes} from '@routing/routes.server';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    provideServerRouting(serverRoutes),
    importProvidersFrom(FlexLayoutServerModule),
  ],
};

export const config = mergeApplicationConfig(appConfig, serverConfig);
