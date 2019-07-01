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
    const clonedProps = JSON.parse(JSON.stringify(this._props));
    for (const propName in clonedProps) {
      if (clonedProps.hasOwnProperty(propName)) {
        this[propName] = clonedProps[propName];
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

  addFilter(field: string, fieldValue: string) {
    const i = this.filters.findIndex(f => f.field === field);

    // Filter has already been set
    if (i > -1) {

      // Make sure it's not a duplicate value
      const j = this.filters[i].value.findIndex(v => v === fieldValue);

      if (j === -1) {
        this.filters[i].value.push(fieldValue);
      }
    } else {
      this.filters.push({ field: field, value: [fieldValue] });
    }
  }

  removeFilter(field: string, fieldValue: string) {
    const i = this.filters.findIndex(f => f.field === field);

    if (i > -1) {
      const j = this.filters[i].value.findIndex(v => v === fieldValue);
      if (j > -1) {
        this.filters[i].value.splice(j, 1);
      }
    }
  }

  replaceFilter(field: string, fieldValue: string) {
    const i = this.filters.findIndex(f => f.field === field);

    if (i === -1) {
      // Filter has not been set yet. Add it.
      this.filters.push({ field: field, value: [fieldValue] });
    } else {
      // Filter has already been set. Completely replace its value.
      this.filters[i].value = [fieldValue];
    }
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
