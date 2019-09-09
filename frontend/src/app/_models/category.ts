export interface Category {
  id: number;
  name: string;
  children: Category[];
  parent_id?: number;
  parent?: Category;
  level: number;
  resource_count?: number;
  study_count?: number;
  training_count?: number;
  hit_count?: number;
  // _links: any;
  // _meta: any;
}
