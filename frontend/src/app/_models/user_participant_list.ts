import { User } from './user';
import { Participant } from './participant';

export interface UserParticipantList {
  user_participants: User[];
  num_self_participants: number;
  num_self_guardians: number;
  num_dependents: number;
  num_self_professionals: number;
  all_participants: [Participant[]];
}
