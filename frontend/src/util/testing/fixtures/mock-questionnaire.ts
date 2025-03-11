import {ParticipantRelationship} from '@models/participantRelationship';
import {IdentificationQuestionnaire} from '@models/questionnaire';

export const mockIdentificationQuestionnaire: IdentificationQuestionnaire = {
  __tablename__: 'identification_questionnaire',
  __label__: 'Identification',
  __question_type__: 'identifying',
  __estimated_duration_minutes__: 5,
  relationship_to_participant_other_hide_expression: '!(model.relationship_to_participant && (model.relationship_to_participant === "other"))',
  id: 1,
  last_updated: new Date(),
  time_on_task_ms: 1,
  participant_id: 1,
  user_id: 1,
  relationship_to_participant: ParticipantRelationship.SELF_PARTICIPANT,
  relationship_to_participant_other: '',
  first_name: '',
  middle_name: '',
  no_middle_name: false,
  last_name: '',
  is_first_name_preferred: false,
  nickname: '',
  birthdate: new Date(),
  birth_city: '',
  birth_state: '',
  is_english_primary: false,
}
