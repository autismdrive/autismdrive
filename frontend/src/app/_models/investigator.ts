import { Organization } from './organization';

export interface Investigator {
  id?: number;
  name: string;
  title: string;
  organization_id: number;
  organization?: Organization;
  bio_link: string;
}
