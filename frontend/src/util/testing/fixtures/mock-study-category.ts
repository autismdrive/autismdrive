import {faker} from '@faker-js/faker';
import {StudyCategory} from '@models/study_category';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockStudy} from '@util/testing/fixtures/mock-study';

export const mockStudyCategory: StudyCategory = {
  id: faker.number.int(),
  category_id: mockCategory.id,
  study_id: mockStudy.id,
  category: mockCategory,
};
