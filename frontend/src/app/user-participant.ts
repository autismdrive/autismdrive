import { Participant } from './participant';
import { User } from './user';

export class UserParticipant {

  static SELF_PARTICIPANT = 'self_participant';
  static SELF_GUARDIAN = 'self_guardian';
  static DEPENDENT = 'dependent';

  id: number;
  participant_id: number;
  user_id: number;
  relationship: String;
  participant: Participant;
  user?: User;
}
