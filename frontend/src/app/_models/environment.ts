export interface AppEnvironment {
  env_name: string;
  production: boolean;
  api: string;
  google_tag_manager_id: string;
  google_maps_api_key: string;
  override_config_url?: string;
}
