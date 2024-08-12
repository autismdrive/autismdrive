import {faker} from '@faker-js/faker';
import {Participant, ParticipantProps} from '@models/participant';
import {ParticipantRelationship} from '@models/participantRelationship';
import {mockUser} from '@util/testing/fixtures/mock-user';

export const makeMockParticipant = (overrideProps?: Partial<ParticipantProps>): Participant => {
  const defaultProps: Partial<ParticipantProps> = {
    id: faker.number.int(),
    user_id: mockUser.id,
    relationship: ParticipantRelationship.SELF_PARTICIPANT,
    last_updated: faker.date.recent(),
    percent_complete: 0,
    name: faker.person.fullName(),
    avatar_color: faker.color.rgb(),
    avatar_icon: 'some_icon',
    has_consented: true,
    step_log: [],
    contact: undefined,
    identification: undefined,
  };

  return new Participant({...defaultProps, ...overrideProps});
};

export const mockParticipant: Participant = makeMockParticipant();
