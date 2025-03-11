import {Optional} from '@angular/core';
import {ParticipantRelationship} from '@models/participantRelationship';

export interface Questionnaire {

}

export interface IdentificationQuestionnaire {
  __tablename__: string;
  __label__: string;
  __question_type__: string;
  __estimated_duration_minutes__: number;
  relationship_to_participant_other_hide_expression: string;
  id: number;
  last_updated: Date;
  time_on_task_ms: number;
  participant_id: number;
  user_id: number;
  relationship_to_participant?: ParticipantRelationship;
  relationship_to_participant_other?: string;
  first_name?: string;
  middle_name?: string;
  no_middle_name?: boolean;
  last_name?: string;
  is_first_name_preferred?: boolean;
  nickname?: string;
  birthdate: Date;
  birth_city?: string;
  birth_state?: string;
  is_english_primary?: boolean;
}

export interface ContactQuestionnaire {

}
export interface ChainQuestionnaire {

}
export interface ClinicalDiagnosesQuestionnaire {

}
export interface CurrentBehaviorsDependentQuestionnaire {

}
export interface CurrentBehaviorsSelfQuestionnaire {

}
export interface DemographicsQuestionnaire {

}
export interface DevelopmentalQuestionnaire {

}
export interface EducationDependentQuestionnaire {

}
export interface EducationSelfQuestionnaire {

}
export interface EmploymentQuestionnaire {

}
export interface EvaluationHistoryDependentQuestionnaire {

}
export interface EvaluationHistorySelfQuestionnaire {

}
export interface HomeDependentQuestionnaire {

}
export interface HomeSelfQuestionnaire {

}
export interface ProfessionalProfileQuestionnaire {

}
export interface RegistrationQuestionnaire {

}
export interface SupportsQuestionnaire {

}
