import {AppEnvironment} from '@models/environment';

// This is the environment file for running the frontend in the local dev environment.
//
// Building with the following flags will override this file with one of the other files
// in this directory:
//
// --configuration=dev --> environment.dev.ts
// --configuration=docker --> environment.docker.ts
// --configuration=staging --> environment.staging.ts
// --configuration=production --> environment.prod.ts
//
// See `angular.json` for more details.

export const SERVICE_HOST = navigator.platform.includes('Win') ? '10.0.2.2' : 'localhost';
export const RESOURCE_API = `http://${SERVICE_HOST}:5000`;

export const environment: AppEnvironment = {
  production: false,
  api: RESOURCE_API,
  google_tag_manager_id: '__GOOGLE_TAG_MANAGER_ID__',
  google_maps_api_key: '__GOOGLE_MAPS_API_KEY__',
  override_config_url: `${RESOURCE_API}/api/config`,
};
