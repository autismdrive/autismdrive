import {Sort} from './query';

export interface SortMethod {
  name: string;
  label: string;
  sortQuery: Sort;
}
