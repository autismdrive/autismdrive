import { GeoLocation } from './geolocation';
import {Category} from './category';
import {HitType} from './hit_type';


export class Query {

  words = '';
  total?: number;
  start = 0;
  size = 20;
  types: String[] = [];
  ages: String[] = [];
  sort: Sort = {
    field: '_score',
    order: 'asc'
  };
  hits?: Array<Hit>;
  category: Category;
  type_counts: Aggregation[] = [];
  age_counts: Aggregation[] = [];
  date?: Date;

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
    const sameTypes = this.types === otherQuery.types;
    const sameAges = this.ages === otherQuery.ages;
    let sameCategory = true;
    if (this.category && otherQuery.category) {
      sameCategory = this.category.id === otherQuery.category.id;
    }
    return (sameWords && sameTypes && sameAges && sameCategory);
  }

  getHitTypes(): HitType[] {
      return HitType.all().filter(t => this.types.includes(t.name));
  }

  hasAgeCounts() {
    return this.age_counts.filter(a => a.count > 0).length > 0;
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
  label: string;
  title: string;
  content: string;
  description: string;
  last_updated: Date;
  date?: Date;
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

export interface Sort {
  field: string;
  order?: string;
  unit?: string;
  latitude?: number;
  longitude?: number;
}


