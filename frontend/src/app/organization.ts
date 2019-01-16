import { Resource } from './resource';
import { Study } from './study';
import { Training } from './training';

export interface Organization {
  id: number;
  name: string;
  description?: string;
  resources?: Resource[];
  studies?: Study[];
  trainings?: Training[];
}
