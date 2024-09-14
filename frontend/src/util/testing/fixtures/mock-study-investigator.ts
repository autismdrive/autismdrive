import {faker} from '@faker-js/faker';
import {StudyInvestigator} from '@models/study_investigator';
import {mockInvestigator} from '@util/testing/fixtures/mock-investigator';
import {mockStudy} from '@util/testing/fixtures/mock-study';

export const mockStudyInvestigator: StudyInvestigator = {
  id: faker.number.int(),
  investigator: mockInvestigator,
  study_id: mockStudy.id,
  investigator_id: mockInvestigator.id,
};
