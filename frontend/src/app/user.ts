import { UserParticipant } from './user-participant';

export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  participants?: UserParticipant[];
}
