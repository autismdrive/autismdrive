import {mockInvestigator} from '@app/shared/fixtures/mock-investigator';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {faker} from '@faker-js/faker';
import {StudyInvestigator} from '@models/study_investigator';

export const mockStudyInvestigator: StudyInvestigator = {
  id: faker.number.int(),
  investigator: mockInvestigator,
  study_id: mockStudy.id,
  investigator_id: mockInvestigator.id,
};
