import { ResourceCategory } from './resource_category';
import { Organization } from './organization';

export interface Location {
  id: number;
  title: string;
  description: string;
  primary_contact: string;
  organization: Organization;
  street_address1: string;
  street_address2: string;
  city: string;
  state: string;
  zip: string;
  phone: string;
  email: string;
  website: string;
  categories: string[];
  status?: string;
  resource_categories?: ResourceCategory[];
}
