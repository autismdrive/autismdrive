import {faker} from '@faker-js/faker';
import {StudyUser} from '@models/study_user';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {mockUser} from '@util/testing/fixtures/mock-user';

export const mockStudyUser: StudyUser = {
  id: faker.number.int(),
  user_id: mockUser.id,
  study_id: mockStudy.id,
  user: mockUser,
  study: mockStudy,
};
