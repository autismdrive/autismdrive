import {Resource} from './resource';
import {User} from './user';

export interface AdminNote {
  id?: number;
  resource_id: number;
  resource?: Resource;
  user_id: number;
  user?: User;
  note: string;
  last_updated?: Date;
}
