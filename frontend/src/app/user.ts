import { Participant } from './participant';
import { ParticipantRelationship } from './participantRelationship';
import { ProfileState } from './profileState';

export class User {

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
    if (participant.relationship === ParticipantRelationship.SELF_GUARDIAN ||
      participant.relationship === ParticipantRelationship.SELF_PARTICIPANT) {
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

  getState() {
    if (this.getSelf() === undefined) {
      return ProfileState.NO_PARTICIPANT;
    } else if (this.getSelf().relationship === ParticipantRelationship.SELF_GUARDIAN) {
      return ProfileState.GUARDIAN;
    } else if (this.getSelf().relationship === ParticipantRelationship.SELF_PARTICIPANT) {
      return ProfileState.PARTICIPANT;
    }
  }

}
