import {Sort} from './query';

export interface SortMethod {
  name: string;
  label: string;
  sortQuery: Sort;
}

export const sortMethods: {[key: string]: SortMethod} = {
  RELEVANCE: {
    name: 'Relevance',
    label: 'Relevance',
    sortQuery: {
      field: '_score',
      order: 'desc',
    },
  },
  DISTANCE: {
    name: 'Distance',
    label: 'Distance',
    sortQuery: {
      field: 'geo_point',
      latitude: null,
      longitude: null,
      order: 'asc',
      unit: 'mi',
    },
  },
  UPDATED: {
    name: 'Updated',
    label: 'Recently Updated',
    sortQuery: {
      field: 'last_updated',
      order: 'desc',
    },
  },
  DATE: {
    name: 'Date',
    label: 'Happening Soon',
    sortQuery: {
      field: 'date',
      order: 'asc',
    },
  },
  DRAFTS: {
    name: 'Drafts',
    label: 'Drafts',
    sortQuery: {
      field: 'is_draft',
      order: 'desc',
    },
  },
};
