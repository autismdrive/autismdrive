import { User } from './user';

export interface UserFavorite {
  id: number;
  type: string;
  user_id: number;
  resource_id?: number;
  category_id?: number;
  age_range?: string;
  language?: string;
  covid19_category?: string;
  user?: User;
}
