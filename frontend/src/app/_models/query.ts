export class Query {
  words = '';
  filters: Array<Filter> = [];
  facets: Array<Facet> = [];
  total?: number;
  size = 20;
  start = 0;
  sort = '_score';
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
}

export class Hit {
  id: number;
  type: string;
  title: string;
  content: string;
  last_updated: Date;
  highlights: string;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}

export interface Filter {
  field: string;
  value: string;
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
