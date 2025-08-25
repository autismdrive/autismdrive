import {mockParticipant} from '@app/shared/fixtures/mock-participant';
import {faker} from '@faker-js/faker';
import {ParticipantAdminList} from '@models/participant_admin_list';

export const mockParticipantAdminList: ParticipantAdminList = {
  num_self_participants: faker.number.int(),
  num_self_guardians: faker.number.int(),
  num_dependents: faker.number.int(),
  num_self_professionals: faker.number.int(),
  filtered_self_participants: faker.number.int(),
  filtered_self_guardians: faker.number.int(),
  filtered_dependents: faker.number.int(),
  filtered_self_professionals: faker.number.int(),
  all_participants: [mockParticipant],
};
