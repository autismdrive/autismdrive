import {ConfigServiceProps} from '@models/config-service-props';

export const mockConfigServiceProps: ConfigServiceProps = {
  apiUrl: 'http://localhost:5000',
  apiKey: 'some_string',
  development: true,
  testing: false,
  mirroring: false,
  production: false,
  googleAnalyticsKey: 'some_string',
}
