import {ConfigServiceProps} from '@services/config/config.service';

export const mockConfigServiceProps: ConfigServiceProps = {
  apiUrl: 'http://localhost:5000',
  apiKey: 'some_string',
  development: true,
  testing: false,
  mirroring: false,
  production: false,
  googleAnalyticsKey: 'some_string',
}
