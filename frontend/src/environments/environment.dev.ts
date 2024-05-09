import {AppEnvironment} from '@models/environment';

export const SERVICE_HOST = 'dev.autismdrive.virginia.edu';

export const environment: AppEnvironment = {
  envName: 'dev',
  production: false,
  api: `https://${SERVICE_HOST}`,
  google_tag_manager_id: 'GOOGLE_TAG_MANAGER_ID',
  google_maps_api_key: 'GOOGLE_MAPS_API_KEY',
};
