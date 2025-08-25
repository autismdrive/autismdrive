import {GoogleMapsMapIds} from '@models/google-maps-api-config';

export interface AppEnvironment {
  development: boolean;
  testing: boolean;
  mirroring: boolean;
  production: boolean;
  apiUrl: string;
  googleAnalyticsTagId: string;
  googleMapsApiKey: string;
  googleMapsMapIds: GoogleMapsMapIds;
}
