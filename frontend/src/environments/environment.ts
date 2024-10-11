import {AppEnvironment} from '@models/environment';

export const SERVICE_HOST = navigator.platform.includes('Win') ? '10.0.2.2' : 'localhost';
export const API_URL = `http://${SERVICE_HOST}:5000`;

const defaultValues: AppEnvironment = {
  env_name: 'local',
  production: false,
  api: API_URL,
  google_tag_manager_id: '__GOOGLE_TAG_MANAGER_ID__',
  google_maps_api_key: '__GOOGLE_MAPS_API_KEY__',
  override_config_url: `${API_URL}/api/config`,
};

export const environment: AppEnvironment = Object.keys(defaultValues).reduce((acc, key) => {
  acc[key] = process.env.hasOwnProperty(key.toUpperCase()) ? process.env[key.toUpperCase()] : defaultValues[key];
  return acc;
}, {} as AppEnvironment);
