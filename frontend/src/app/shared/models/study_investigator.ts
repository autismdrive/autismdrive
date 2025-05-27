import {Investigator} from './investigator';

export interface StudyInvestigator {
  id?: number;
  investigator?: Investigator;
  study_id: number;
  investigator_id: number;
}
