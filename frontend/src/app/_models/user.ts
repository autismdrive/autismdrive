import { Participant } from './participant';
import { ParticipantRelationship } from './participantRelationship';
import { EmailLog } from './email_log';
import { UserFavorite } from './user_favorite';
import {UserMeta} from './user_meta';

export class User {

  id: number;
  email: string;
  participants?: Participant[];
  user_meta?: UserMeta;
  user_favorites?: UserFavorite[];
  last_updated?: Date;
  registration_date?: Date;
  last_login?: Date;
  token?: string;
  role?: string;
  permissions?: string[];
  email_log?: EmailLog[];
  token_url?: string;
  participant_count?: number;
  created_password: boolean;
  identity: string;
  percent_self_registration_complete: number;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
    if (this.participants && (this.participants.length > 0)) {
      this.participants = this.participants.map(p => new Participant(p));
    }
    if (this.user_meta) {
      this.user_meta = new UserMeta(this.user_meta);
    }
  }

  isSelf(participant: Participant): boolean {
    if (participant.relationship === ParticipantRelationship.SELF_GUARDIAN ||
      participant.relationship === ParticipantRelationship.SELF_PARTICIPANT ||
      participant.relationship === ParticipantRelationship.SELF_PROFESSIONAL ||
      participant.relationship === ParticipantRelationship.SELF_INTERESTED) {
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

  getParticipantById(participantId: number): Participant  {
    for (const p of this.participants) {
      if (p.id === participantId) {
        return p;
      }
    }
    throw Error('The user does not have a participant with the given id.');
  }

  hasContactInfo(participant: Participant): boolean {
     return participant.contact != null;
  }

  checkContact() {
    return this.participants.find(p => this.hasContactInfo(p)) != null;
  }

}
