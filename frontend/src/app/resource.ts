import { ResourceCategory } from './resource_category';

export interface Resource {
  id: number;
  title: string;
  description: string;
  image: string;
  imageCaption: string;
  organization: string;
  streetAddress1: string;
  streetAddress2: string;
  city: string;
  state: string;
  zip: string;
  county: string;
  phone: string;
  website: string;
  categories: string[];
  status?: string;
  resource_categories?: ResourceCategory[];
}
