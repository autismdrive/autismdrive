import {inject} from '@angular/core';
import {GoogleModuleOptions} from '@ng-maps/google';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';

export const googleMapsApiConfigFactory = (): GoogleModuleOptions => {
  const appEnvironment = inject(AppEnvironmentService);
  console.log('googleMapsApiConfigFactory > appEnvironment', appEnvironment);
  const googleMapsApiKey = appEnvironment.googleMapsApiKey;

  if (googleMapsApiKey) {
    return {
      apiKey: googleMapsApiKey,
      libraries: ['maps', 'marker', 'places', 'geocoding'],
    };
  }
  throw new Error('API URL not found in configuration');
};
