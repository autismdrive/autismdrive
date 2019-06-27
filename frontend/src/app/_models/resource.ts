import { ResourceCategory } from './resource_category';
import { Organization } from './organization';

export interface Resource {
  id: number;
  title: string;
  description: string;
  organization: Organization;
  phone: string;
  website: string;
  categories: string[];
  last_updated: string;
  status?: string;
  resource_categories?: ResourceCategory[];
}
