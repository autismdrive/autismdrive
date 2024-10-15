import {Category} from './category';
import {GeoLocation} from './geolocation';
import {HitType} from './hit_type';

export interface GeoPoint {
  lat: number;
  lon: number;
}

export interface GeoBox {
  top_left: GeoPoint;
  bottom_right: GeoPoint;
}

export interface QueryProps {
  words?: string;
  total?: number;
  start?: number;
  size?: number;
  types?: String[];
  ages?: String[];
  languages?: String[];
  sort?: Sort;
  hits?: Hit[];
  category?: Category;
  type_counts?: Aggregation[];
  age_counts?: Aggregation[];
  language_counts?: Aggregation[];
  date?: Date;
  status?: string;
  map_data_only?: boolean;
  geo_box: GeoBox;
}

export class Query {
  words = '';
  total?: number;
  start = 0;
  size = 20;
  types: String[] = [];
  ages: String[] = [];
  languages: String[] = [];
  sort: Sort = {
    field: '_score',
    order: 'asc',
  };
  hits?: Array<Hit> = [];
  category: Category;
  type_counts: Aggregation[] = [];
  age_counts: Aggregation[] = [];
  language_counts: Aggregation[] = [];
  date?: Date;
  status?: string;
  map_data_only = false;
  geo_box: GeoBox;

  constructor(private _props: QueryProps) {
    const clonedProps = JSON.parse(JSON.stringify(this._props));
    for (const propName in clonedProps) {
      if (clonedProps.hasOwnProperty(propName)) {
        this[propName] = clonedProps[propName];
      }
    }

    if (this.hits && this.hits.length > 0) {
      this.hits = this.hits.map(h => new Hit(h));
    }
  }

  public get hasHits(): boolean {
    return !!(this.hits && this.hits.length > 0);
  }

  public get hasWords(): boolean {
    return !!(this.words && this.words.length > 0);
  }

  public get hasTypes(): boolean {
    return !!(this.types && (this.types.length === 1 || this.types.length === 2));
  }

  public get hasAges(): boolean {
    return !!(this.ages && this.ages.length > 0);
  }

  public get hasLanguages(): boolean {
    return !!(this.languages && this.languages.length > 0);
  }

  public get hasCategory(): boolean {
    return !!(this.category && this.category.id);
  }

  public get hasFilters(): boolean {
    return !!(this.hasWords || this.hasTypes || this.hasLanguages || this.hasAges || this.hasCategory);
  }

  public get hitTypes(): HitType[] {
    return HitType.all().filter(t => this.types.includes(t.name));
  }

  public get hasAgeCounts() {
    return this.age_counts.filter(a => a.count > 0).length > 0;
  }

  public get hasLanguageCounts() {
    return this.language_counts.filter(a => a.count > 0).length > 0;
  }

  equals(otherQuery: Query) {
    const sameWords = this.words === otherQuery.words;
    const sameTypes = this.types === otherQuery.types;
    const sameAges = this.ages === otherQuery.ages;
    const sameLanguages = this.languages === otherQuery.languages;
    let sameCategory = true;
    if (this.category && otherQuery.category) {
      sameCategory = this.category.id === otherQuery.category.id;
    }
    return sameWords && sameTypes && sameAges && sameLanguages && sameCategory;
  }
}

export class Aggregation {
  value: string;
  count: number;
  is_selected: Boolean;
}

export class Hit extends GeoLocation {
  type: string;
  ages: string[];
  languages: string[];
  label: string;
  title: string;
  content: string;
  description: string;
  post_event_description: string;
  last_updated: Date;
  date?: Date;
  highlights: string;
  url?: string;
  status?: string;
  is_draft?: boolean;

  constructor(private _props) {
    super(_props);

    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}

export interface Sort {
  field: string;
  order?: string;
  unit?: string;
  latitude?: number;
  longitude?: number;
}
