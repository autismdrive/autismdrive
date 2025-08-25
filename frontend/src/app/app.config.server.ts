import {ApplicationConfig, importProvidersFrom, mergeApplicationConfig} from '@angular/core';
import {provideServerRendering} from '@angular/platform-server';
import {provideServerRouting} from '@angular/ssr';
import {LOCAL_STORAGE} from '@app/tokens';
import {FlexLayoutServerModule} from '@ngbracket/ngx-layout/server';
import {serverRoutes} from '@routing/routes.server';
import {appConfig} from './app.config';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    {
      provide: LOCAL_STORAGE,
      useFactory: () => ({
        getItem: () => {},
        setItem: () => {},
        removeItem: () => {},
      }),
    },
    provideServerRouting(serverRoutes),
    importProvidersFrom(FlexLayoutServerModule),
  ],
};

export const config = mergeApplicationConfig(appConfig, serverConfig);
