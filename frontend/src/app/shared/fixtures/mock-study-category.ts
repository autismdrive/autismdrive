import {mockCategory} from '@app/shared/fixtures/mock-category';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {faker} from '@faker-js/faker';
import {StudyCategory} from '@models/study_category';

export const mockStudyCategory: StudyCategory = {
  id: faker.number.int(),
  category_id: mockCategory.id,
  study_id: mockStudy.id,
  category: mockCategory,
};
