import {faker} from '@faker-js/faker';
import {mockGoogleMapsMapIdsFactory} from '@fixtures/mock-google-maps-config';
import {AppEnvironment} from '@models/environment';

export const mockAppEnvironment: AppEnvironment = {
  apiUrl: 'http://localhost:5000',
  development: true,
  testing: false,
  mirroring: false,
  production: false,
  googleAnalyticsTagId: faker.string.uuid(),
  googleMapsApiKey: faker.string.uuid(),
  googleMapsMapIds: mockGoogleMapsMapIdsFactory(),
};
