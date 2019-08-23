import { ParticipantRelationship } from './participantRelationship';
import { StepLog } from './step_log';
import { ContactQ } from './contact_q';

export class Participant {
  id?: number;
  user_id: number;
  relationship: string;
  last_updated?: Date;
  percent_complete?: number;
  num_studies_enrolled?: number;
  name?: string;
  avatar_color?: string;
  avatar_icon?: string;
  has_consented: boolean;
  step_log?: StepLog[];
  contact?: ContactQ;

  constructor(private _props) {
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
      case ParticipantRelationship.SELF_PARTICIPANT:
        return 'self_intake';
      default:
        return 'self_intake';
    }
  }
}
