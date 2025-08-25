import {InjectionToken} from '@angular/core';
import {GoogleMapsApiConfig, GoogleMapsMapIds} from '@models/google-maps-api-config';
export const LOCAL_STORAGE = new InjectionToken<Storage>('Local Storage');
export const GOOGLE_MAPS_API_CONFIG = new InjectionToken<GoogleMapsApiConfig>('Google Maps API Config');
export const GOOGLE_MAPS_MAP_IDS = new InjectionToken<GoogleMapsMapIds>('Google Maps Map IDS');
