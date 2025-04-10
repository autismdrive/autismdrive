import {AppEnvironment} from '@models/environment';

export const environment: AppEnvironment = {
  development: true,
  testing: false,
  mirroring: false,
  production: false,
  apiUrl: 'http://localhost:5000',
  googleAnalyticsTagId: '__GOOGLE_ANALYTICS_TAG_ID__',
  googleMapsApiKey: '__GOOGLE_MAPS_API_KEY__',
};
