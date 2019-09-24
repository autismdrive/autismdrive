import {Resource} from './resource';
import {Study} from './study';

export interface RelatedOptions {
  resource_id: number;
  study_id: number;
}

export interface RelatedResults {
  resources: Resource[];
  studies: Study[];
}
