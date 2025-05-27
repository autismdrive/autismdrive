import {Participant} from './participant';

export interface ParticipantAdminList {
  num_self_participants: number;
  num_self_guardians: number;
  num_dependents: number;
  num_self_professionals: number;
  filtered_self_participants: number;
  filtered_self_guardians: number;
  filtered_dependents: number;
  filtered_self_professionals: number;
  all_participants: Participant[];
}
