import { UserParticipant } from './user-participant';

export interface User {
  id: number;
  email: string;
  role: string;
  participants?: UserParticipant[];
  last_updated: Date;
}
