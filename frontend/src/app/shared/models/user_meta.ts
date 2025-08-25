import {ParticipantRelationship} from './participantRelationship';

export class UserMeta {
  id: number;
  last_updated?: Date;
  self_participant?: boolean;
  self_has_guardian?: boolean;
  guardian?: boolean;
  guardian_has_dependent?: boolean;
  professional?: boolean;
  interested?: boolean;
  self_relationship: ParticipantRelationship;

  constructor(_props: {}) {
    for (const propName in _props) {
      if (_props.hasOwnProperty(propName)) {
        this[propName] = _props[propName];
      }
    }
  }
}
