export interface Query {
  query: string;
  filters: Array<Filter>;
  facets: Array<Facet>;
  total?: number;
  size: number;
  start: number;
  sort?: string;
  hits?: Array<Hit>;
}

export interface Hit {
  id: number;
  type: string;
  title: string;
  content: string;
  last_updated: Date;
  highlights: string;
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
