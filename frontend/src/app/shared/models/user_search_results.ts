import {User} from './user';

export interface UserSearchResults {
  pages: number;
  total: number;
  items: User[];
}
