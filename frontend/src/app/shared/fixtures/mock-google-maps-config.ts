import {faker} from '@faker-js/faker';
import {GoogleMapsApiConfig, GoogleMapsLibrary, GoogleMapsMapIds} from '@models/google-maps-api-config';
import {sampleSize} from 'lodash-es';

export const mockGoogleMapsMapIdsFactory = (override?: Partial<GoogleMapsMapIds>): GoogleMapsMapIds => {
  const defaultValues: GoogleMapsMapIds = {
    resourceDetailsPage: faker.string.uuid(),
    searchPage: faker.string.uuid(),
  };
  return (
    override
      ? {
          ...defaultValues,
          ...override,
        }
      : defaultValues
  ) as GoogleMapsMapIds;
};

export const mockGoogleMapsApiConfigFactory = (override?: Partial<GoogleMapsApiConfig>): GoogleMapsApiConfig => {
  const defaultValues: GoogleMapsApiConfig = {
    apiKey: faker.string.uuid(),
    libraries: sampleSize(Object.values(GoogleMapsLibrary), 5) as GoogleMapsLibrary[],
  };

  return (
    override
      ? {
          ...defaultValues,
          ...override,
        }
      : defaultValues
  ) as GoogleMapsApiConfig;
};
