import {Category} from './category';

export interface StudyCategory {
  id?: number;
  category_id: number;
  study_id: number;
  category?: Category;
}
