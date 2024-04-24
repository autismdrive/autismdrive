import {AppEnvironment} from '@shared/types/environment';

export const SERVICE_HOST = 'staging.autismdrive.virginia.edu';
export const RESOURCE_API = `https://${SERVICE_HOST}`;

export const environment: AppEnvironment = {
  envName: 'staging',
  production: true,
  api: RESOURCE_API,
  google_tag_manager_id: 'GOOGLE_TAG_MANAGER_ID',
  google_maps_api_key: 'GOOGLE_MAPS_API_KEY',
};
