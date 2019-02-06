import { User } from './user';

export class Participant {
  id: number;
  last_updated?: Date;
  first_name: string;
  last_name: string;
  users?: User[];

  nickname?: string;
  percent_complete?: number;
  num_studies_enrolled?: number;
  avatar_img_url?: string;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }

  public preferredName() {
    return `${this.nickname || this.first_name} ${this.last_name}`;
  }

}
