import { StudyCategory } from './study_category';
import { StudyInvestigator } from './study_investigator';

export interface Study {
  id: number;
  title: string;
  description: string;
  participant_description: string;
  benefit_description
  investigators: string[];
  organization_id: number;
  location: string;
  categories: string[];
  status: string;
  study_categories?: StudyCategory[];
  study_investigators?: StudyInvestigator[];
}
