import { User } from './user';
import { Study } from './study';

export interface StudyUser {
  id: number;
  user_id: number;
  study_id: number;
  user?: User;
  study?: Study;
}
