import { ResourceCategory } from './resource_category';
import { Organization } from './organization';

export interface Event {
  id: number;
  title: string;
  description: string;
  date: string;
  time: string;
  ticket_cost: string;
  organization: Organization;
  primary_contact: string;
  location_name: string;
  street_address1: string;
  street_address2: string;
  city: string;
  state: string;
  zip: string;
  phone: string;
  website: string;
  categories: string[];
  last_updated: string;
  status?: string;
  resource_categories?: ResourceCategory[];
}
