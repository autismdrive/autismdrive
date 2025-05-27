import {Category} from './category';

export interface ResourceCategory {
  id?: number;
  category_id: number;
  resource_id: number;
  type: string;
  category?: Category;
}
