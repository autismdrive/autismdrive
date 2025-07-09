/**
 * Loads the configuration from the middleware, which should be running on localhost port 5000.
 */
import {HttpBackend, HttpEvent, HttpEventType, HttpRequest} from '@angular/common/http';
import {inject} from '@angular/core';
import {AppEnvironment} from '@models/environment';
import {GoogleMapsApiConfig, GoogleMapsLibrary} from '@models/google-maps-api-config';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {StorageService} from '@services/storage/storage.service';
import {catchError, map} from 'rxjs';

export const CONFIG_URL = 'http://localhost:5000/api/config';

export const appInitializer = () => {
  const httpBackend = inject(HttpBackend);
  const storageService = inject(StorageService);
  const appEnvironmentService = inject(AppEnvironmentService);

  // We have to use HttpBackend instead of HttpClient to avoid circular dependencies
  // with the HttpInterceptors, which depend on having the config already loaded.
  return httpBackend.handle(new HttpRequest('GET', CONFIG_URL, {responseType: 'json'})).pipe(
    map((r: HttpEvent<any>) => {
      if (r.type === HttpEventType.Response) {
        const appEnvironment: AppEnvironment = r.body;
        storageService.set('appEnvironment', JSON.stringify(appEnvironment));
        appEnvironmentService.fromProperties(appEnvironment);
        storageService.set(
          'googleMapsApiConfig',
          JSON.stringify({
            apiKey: appEnvironment.googleMapsApiKey,
            libraries: [
              GoogleMapsLibrary.CoreLibrary,
              GoogleMapsLibrary.MapsLibrary,
              GoogleMapsLibrary.MarkerLibrary,
              GoogleMapsLibrary.PlacesLibrary,
              GoogleMapsLibrary.GeocodingLibrary,
            ],
          } as GoogleMapsApiConfig),
        );
        storageService.set('googleMapsMapIds', JSON.stringify(appEnvironment.googleMapsMapIds));
      }
    }),
    catchError((error: any) => {
      console.error('Error loading configuration:', error);
      throw error;
    }),
  );
};
