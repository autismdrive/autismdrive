import {Study} from './study';
import {User} from './user';

export interface StudyUser {
  id: number;
  user_id: number;
  study_id: number;
  user?: User;
  study?: Study;
}
