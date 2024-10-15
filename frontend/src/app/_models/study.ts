import {StudyCategory} from './study_category';
import {StudyInvestigator} from './study_investigator';

export enum StudyStatus {
  currently_enrolling = 'Currently enrolling',
  study_in_progress = 'Study in progress',
  results_being_analyzed = 'Results being analyzed',
  study_results_published = 'Study results published',
}

export interface StudyProps {
  id?: number;
  title: string;
  short_title?: string;
  description: string;
  short_description?: string;
  participant_description?: string;
  benefit_description?: string;
  investigators: string[];
  organization_name?: string;
  location: string;
  categories: string[];
  status: StudyStatus;
  num_visits?: number;
  coordinator_email?: string;
  study_categories?: StudyCategory[];
  study_investigators?: StudyInvestigator[];
  image_url?: string;
  eligibility_url?: string;
  survey_url?: string;
  results_url?: string;
  ages?: string[];
  languages?: string[];
  last_updated?: Date;
}

export class Study {
  id?: number;
  title: string;
  short_title?: string;
  description: string;
  short_description?: string;
  participant_description?: string;
  benefit_description?: string;
  investigators: string[];
  organization_name?: string;
  location: string;
  categories: string[];
  status: string;
  num_visits?: number;
  coordinator_email?: string;
  study_categories?: StudyCategory[];
  study_investigators?: StudyInvestigator[];
  image_url?: string;
  eligibility_url?: string;
  survey_url?: string;
  results_url?: string;
  ages?: string[];
  languages?: string[];
  last_updated?: Date;

  constructor(private _props: StudyProps) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}
