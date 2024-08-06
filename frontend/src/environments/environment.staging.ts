import {AppEnvironment} from '@models/environment';

export const SERVICE_HOST = 'staging.autismdrive.virginia.edu';
export const RESOURCE_API = `https://${SERVICE_HOST}`;

export const environment: AppEnvironment = {
  envName: 'staging',
  production: true,
  api: RESOURCE_API,
  google_tag_manager_id: '__GOOGLE_TAG_MANAGER_ID__',
  google_maps_api_key: '__GOOGLE_MAPS_API_KEY__',
};
