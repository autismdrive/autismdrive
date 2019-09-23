import { User } from './user';
import { Resource } from './resource';

export interface AdminNote {
  id?: number;
  resource_id: number;
  resource?: Resource;
  user_id: number;
  user?: User;
  note: string;
  last_updated?: Date;
}
