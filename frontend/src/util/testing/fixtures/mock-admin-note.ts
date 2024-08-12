import {AdminNote} from '@app/_models/admin_note';
import {faker} from '@faker-js/faker';
import {mockResource} from '@util/testing/fixtures/mock-resource';
import {mockUser} from './mock-user';

export const makeMockAdminNote = (overrideProps?: Partial<AdminNote>): AdminNote => {
  const defaultProps: AdminNote = {
    id: faker.number.int(),
    resource_id: mockResource.id,
    resource: mockResource,
    user_id: mockUser.id,
    user: mockUser,
    note: faker.lorem.sentence(),
    last_updated: faker.date.recent(),
  };
  return {...defaultProps, ...overrideProps};
};

export const mockAdminNote = makeMockAdminNote();
