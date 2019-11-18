import { StudyCategory } from './study_category';
import { StudyInvestigator } from './study_investigator';
import { Organization } from './organization';

export enum StudyStatus {
  currently_enrolling = 'Currently enrolling',
  study_in_progress = 'Study in progress',
  results_being_analyzed = 'Results being analyzed',
  study_results_published = 'Study results published',
}

export interface Study {
  id?: number;
  title: string;
  short_title?: string;
  description: string;
  short_description?: string;
  participant_description: string;
  benefit_description: string;
  investigators: string[];
  organization_id?: number;
  organization?: Organization;
  location: string;
  categories: string[];
  status: string;
  study_categories?: StudyCategory[];
  study_investigators?: StudyInvestigator[];
  image_url?: string;
  eligibility_url?: string;
  ages?: string[];
}
