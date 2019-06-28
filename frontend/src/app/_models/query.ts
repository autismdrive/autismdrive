import { GeoLocation } from './geolocation';

export class Query {
  words = '';
  filters: Array<Filter> = [];
  facets: Array<Facet> = [];
  total?: number;
  size = 20;
  start = 0;
  sort: Sort = {
    field: '_score',
    order: 'asc'
  };
  hits?: Array<Hit>;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }

    if (this.hits && (this.hits.length > 0)) {
      this.hits = this.hits.map(h => new Hit(h));
    }
  }

  equals(otherQuery: Query) {
    const sameWords = this.words === otherQuery.words;
    const sameFilters = this.filters.toString() === otherQuery.filters.toString();
    return (sameWords && sameFilters);
  }
}

export enum HitType {
  LOCATION = 'LOCATION',
  RESOURCE = 'RESOURCE',
  STUDY = 'STUDY',
  EVENT = 'EVENT'
}

export enum HitLabel {
  LOCATION = 'Local Services',
  RESOURCE = 'Online Information',
  STUDY = 'Research Studies',
  EVENT = 'Events and Training'
}

export class Hit extends GeoLocation {
  id: number;
  type: string;
  label: string;
  title: string;
  content: string;
  description: string;
  last_updated: Date;
  highlights: string;
  url?: string;

  constructor(private _props) {
    super(_props);

    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}

export interface Filter {
  field: string;
  value: string[];
}

export interface Sort {
  field: string;
  order?: string;
  unit?: string;
  latitude?: number;
  longitude?: number;
}

export interface Facet {
  field: string;
  facetCounts: Array<FacetCount>;
}

export interface FacetCount {
  category: string;
  hit_count: number;
  is_selected: boolean;
}
