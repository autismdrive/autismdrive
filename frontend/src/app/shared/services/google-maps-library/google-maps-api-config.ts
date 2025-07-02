import {inject} from '@angular/core';
import {GoogleMapsApiConfig, GoogleMapsMapIds} from '@models/google-maps-api-config';
import {StorageService} from '@services/storage/storage.service';

export const googleMapsApiConfigFactory = (): GoogleMapsApiConfig => {
  const storageService = inject(StorageService);
  const googleMapsApiConfig = storageService.get('googleMapsApiConfig');

  if (googleMapsApiConfig?.length > 0) {
    return JSON.parse(googleMapsApiConfig) as GoogleMapsApiConfig;
  }

  throw new Error('Google Maps API configuration not found in local storage. Please ensure it is set up correctly.');
};

export const googleMapsMapIdsFactory = (): GoogleMapsMapIds => {
  const storageService = inject(StorageService);
  const googleMapsMapIds = storageService.get('googleMapsMapIds');

  if (googleMapsMapIds?.length > 0) {
    return JSON.parse(googleMapsMapIds) as GoogleMapsMapIds;
  }

  throw new Error('Google Maps Map IDs not found in local storage. Please ensure it is set up correctly.');
};
