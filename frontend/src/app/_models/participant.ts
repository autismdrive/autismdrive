import {User} from '@models/user';
import {ContactQ} from './contact_q';
import {IdentificationQ} from './identification_q';
import {ParticipantRelationship} from './participantRelationship';
import {StepLog} from './step_log';

export interface ParticipantProps {
  id?: number;
  user_id: number;
  user?: User;
  relationship: ParticipantRelationship;
  last_updated?: Date;
  percent_complete?: number;
  name?: string;
  avatar_color?: string;
  avatar_icon?: string;
  has_consented: boolean;
  step_log?: StepLog[];
  contact?: ContactQ;
  identification?: IdentificationQ;
}

export class Participant {
  id?: number;
  user_id: number;
  user?: User;
  relationship: ParticipantRelationship;
  last_updated?: Date;
  percent_complete?: number;
  name?: string;
  avatar_color?: string;
  avatar_icon?: string;
  has_consented: boolean;
  step_log?: StepLog[];
  contact?: ContactQ;
  identification?: IdentificationQ;

  constructor(private _props: Partial<ParticipantProps>) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }

  getFlowName(): string {
    switch (this.relationship) {
      case ParticipantRelationship.DEPENDENT:
        return 'dependent_intake';
      case ParticipantRelationship.SELF_GUARDIAN:
        return 'guardian_intake';
      case ParticipantRelationship.SELF_PROFESSIONAL:
        return 'professional_intake';
      case ParticipantRelationship.SELF_INTERESTED:
        return 'interested_intake';
      case ParticipantRelationship.SELF_PARTICIPANT:
        return 'self_intake';
      default:
        return 'self_intake';
    }
  }
}
