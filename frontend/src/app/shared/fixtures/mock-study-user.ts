import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {faker} from '@faker-js/faker';
import {StudyUser} from '@models/study_user';

export const mockStudyUser: StudyUser = {
  id: faker.number.int(),
  user_id: mockUser.id,
  study_id: mockStudy.id,
  user: mockUser,
  study: mockStudy,
};
