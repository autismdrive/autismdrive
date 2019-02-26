import { User } from './user';

export class Participant {
  id?: number;
  user_id: number;
  // user: User;
  relationship: String;
  last_updated?: Date;
  percent_complete?: number;
  num_studies_enrolled?: number;
  avatar_img_url?: string;
  name?: string;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }

  getFlowName(): string {
    switch (this.relationship) {
      case User.DEPENDENT:
        return 'dependent_intake';
      case User.SELF_GUARDIAN:
        return 'guardian_intake';
      case User.SELF_PARTICIPANT:
        return 'self_intake';
      default:
        return 'self_intake';
    }
  }
}
