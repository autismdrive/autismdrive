import {faker} from '@faker-js/faker';
import {ParticipantRelationship} from '@models/participantRelationship';
import {User} from '@models/user';
import {UserMeta} from '@models/user_meta';

export const mockUserMeta: UserMeta = {
  id: faker.number.int(),
  last_updated: faker.date.recent(),
  self_participant: true,
  self_has_guardian: false,
  guardian: false,
  guardian_has_dependent: false,
  professional: false,
  interested: true,
  self_relationship: ParticipantRelationship.SELF_PARTICIPANT,
};

export const mockUser: User = new User({
  id: faker.number.int(),
  email: faker.internet.email(),
  participants: [],
  user_meta: mockUserMeta,
  user_favorites: [],
  last_updated: faker.date.recent(),
  registration_date: faker.date.recent(),
  last_login: faker.date.recent(),
  token: '',
  role: '',
  permissions: [],
  email_log: [],
  token_url: '',
  participant_count: 0,
  created_password: true,
  identity: '',
  percent_self_registration_complete: 0,
});
