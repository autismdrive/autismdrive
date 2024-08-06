import {AppEnvironment} from '@models/environment';

// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.
export const SERVICE_HOST = navigator.platform.includes('Win') ? '10.0.2.2' : 'localhost';

export const environment: AppEnvironment = {
  envName: 'docker',
  production: false,
  api: `http://${SERVICE_HOST}`,
  google_tag_manager_id: '__GOOGLE_TAG_MANAGER_ID__',
  google_maps_api_key: '__GOOGLE_MAPS_API_KEY__',
};
