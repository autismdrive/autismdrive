import { Participant } from './participant';
import { User } from './user';

export interface UserParticipant {
  id: number;
  participant_id: number;
  user_id: number;
  participant: Participant;
  user: User;
  relationship: string;
}
