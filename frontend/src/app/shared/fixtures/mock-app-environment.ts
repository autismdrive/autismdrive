import {AppEnvironment} from '@models/environment';

export const mockAppEnvironment: AppEnvironment = {
  apiUrl: 'http://localhost:5000',
  development: true,
  testing: false,
  mirroring: false,
  production: false,
  googleAnalyticsTagId: 'some_string',
  googleMapsApiKey: 'some_string',
};
