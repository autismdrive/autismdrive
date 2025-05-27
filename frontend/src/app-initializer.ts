/**
 * Loads the configuration from the middleware, which should be running on localhost port 5000.
 */
import {HttpBackend, HttpEvent, HttpEventType, HttpRequest} from '@angular/common/http';
import {inject, InjectionToken, runInInjectionContext} from '@angular/core';
import {GoogleModuleOptions} from '@ng-maps/google';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {googleMapsApiConfigFactory} from '@services/google-maps-library/google-maps-api-config';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';
import {StorageService} from '@services/storage/storage.service';
import {catchError, map} from 'rxjs';

export const CONFIG_URL = 'http://localhost:5000/api/config';

export const appInitializer = () => {
  console.log('appInitializer');
  const httpBackend = inject(HttpBackend);
  const storageService = inject(StorageService);
  const appEnvironmentService = inject(AppEnvironmentService);

  // We have to use HttpBackend instead of HttpClient to avoid circular dependencies
  // with the HttpInterceptors, which depend on having the config already loaded.
  return httpBackend.handle(new HttpRequest('GET', CONFIG_URL, {responseType: 'json'})).pipe(
    map((r: HttpEvent<any>) => {
      if (r.type === HttpEventType.Response) {
        const appEnvironment = r.body;
        console.log('appInitializer > config endpoint response:', {appEnvironment});
        storageService.set('appEnvironment', JSON.stringify(appEnvironment));
        appEnvironmentService.fromProperties(appEnvironment);
        storageService.set(
          'googleModuleOptions',
          JSON.stringify({
            apiKey: appEnvironment.googleMapsApiKey,
            libraries: ['maps', 'marker', 'places', 'geocoding'],
          }),
        );
      }
    }),
    catchError((error: any) => {
      console.error('Error loading configuration:', error);
      throw error;
    }),
  );
};
