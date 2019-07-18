import { Resource } from './resource';
import { Study } from './study';

export interface Organization {
  id?: number;
  name: string;
  description?: string;
  resources?: Resource[];
  studies?: Study[];
}
