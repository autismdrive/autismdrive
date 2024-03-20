import {Category} from './category';
import {Resource} from './resource';
import {User} from './user';

export class UserFavorite {
  id: number;
  type: string;
  user_id: number;
  resource_id?: number;
  resource?: Resource;
  category_id?: number;
  category?: Category;
  age_range?: string;
  language?: string;
  covid19_category?: string;
  user?: User;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}
