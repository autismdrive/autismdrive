import {CdkTreeNode} from '@angular/cdk/tree';
import {Observable} from 'rxjs';

export interface Category {
  id?: number;
  name?: string;
  children?: Category[];
  parent_id?: number;
  parent?: Category;
  level?: number;
  all_resource_count?: number;
  resource_count?: number;
  event_count?: number;
  location_count?: number;
  study_count?: number;
  hit_count?: number;
  display_order?: number;
  indentedString?: string;
}

export type CategoriesById = Record<number, Category>;

export type CategoriesByDisplayOrder = Record<string, Category>;
export type CatTreeNode = CdkTreeNode<Category, Category>;
export type CatTreeNodeList = CatTreeNode[] | Observable<CatTreeNode[]>;
