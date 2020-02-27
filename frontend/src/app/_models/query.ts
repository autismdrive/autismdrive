import {GeoLocation} from './geolocation';
import {Category} from './category';
import {HitType} from './hit_type';


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
    order: 'asc'
  };
  hits?: Array<Hit> = [];
  category: Category;
  type_counts: Aggregation[] = [];
  age_counts: Aggregation[] = [];
  language_counts: Aggregation[] = [];
  date?: Date;
  status?: string;
  map_data_only = false;

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

  hasFilters() {
    const hasWords = this.words && (this.words.length > 0);
    return hasWords || this.types.length > 0 ||
      this.ages.length > 0 || this.languages.length > 0 ||
      this.category;
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
    return (sameWords && sameTypes && sameAges && sameLanguages && sameCategory);
  }

  getHitTypes(): HitType[] {
      return HitType.all().filter(t => this.types.includes(t.name));
  }

  hasAgeCounts() {
    return this.age_counts.filter(a => a.count > 0).length > 0;
  }

  hasLanguageCounts() {
    return this.language_counts.filter(a => a.count > 0).length > 0;
  }

}

export class Aggregation {
  value: string;
  count: number;
  is_selected: Boolean;
}

export class Hit extends GeoLocation {
  id: number;
  type: string;
  ages: string[];
  languages: string[];
  label: string;
  title: string;
  content: string;
  description: string;
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


