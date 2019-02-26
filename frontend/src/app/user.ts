import { Participant } from './participant';


export class User {

  static SELF_PARTICIPANT = 'self_participant';
  static SELF_GUARDIAN = 'self_guardian';
  static DEPENDENT = 'dependent';

  id: number;
  email: string;
  role: string;
  relationship?: string;
  participants?: Participant[];
  last_updated?: Date;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }

    if (this.participants && (this.participants.length > 0)) {
      this.participants = this.participants.map(p => new Participant(p));
    }
  }

  hasSelf() {
    return this.getSelf() !== null;
  }

  isSelf(participant: Participant): boolean {
    if (participant.relationship === User.SELF_GUARDIAN ||
      participant.relationship === User.SELF_PARTICIPANT) {
      return true;
    } else {
      return false;
    }
  }

  getSelf(): Participant {
    return this.participants.find(p => this.isSelf(p));
  }

  getDependents() {
    return this.participants.filter(p => !this.isSelf(p));
  }

}
