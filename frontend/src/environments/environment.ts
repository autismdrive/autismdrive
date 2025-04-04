import {AppEnvironment} from '@models/environment';

export const SERVICE_HOST = navigator.platform.includes('Win') ? '10.0.2.2' : 'localhost';
export const API_URL = `http://${SERVICE_HOST}:5000`;

export const environment: AppEnvironment = {
  envName: 'local',
  production: false,
  api: API_URL,
  googleTagManagerId: 'GTM-NXC9K3FK',
  googleMapsApiKey: 'AIzaSyDrjVhrMx_xwSnImf7D7Rjgcp6rAc4NA8Q',
};
