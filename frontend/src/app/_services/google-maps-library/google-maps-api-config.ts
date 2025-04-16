import {inject} from '@angular/core';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';

export const googleMapsApiConfigFactory = (): any => {
  const appEnvironment = inject(AppEnvironmentService);
  console.log(appEnvironment.googleMapsApiKey);
  const googleMapsApiKey = appEnvironment.googleMapsApiKey;
  if (googleMapsApiKey) {
    console.log('set apiUrl');
    return {
      apiKey: googleMapsApiKey,
      libraries: ['maps', 'marker', 'geocoding'],
    };
  }
  throw new Error('API URL not found in configuration');
};
