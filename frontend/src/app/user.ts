import { UserParticipant } from './user-participant';
import {Participant} from './participant';


export class User {
  id: number;
  email: string;
  role: string;
  participants?: UserParticipant[];
  last_updated?: Date;

  constructor(id: number, email: string, role: string) {
    this.id = id;
    this.email = email;
    this.role = role;
  }

  hasSelf() {
    return this.getSelf() !== null;
  }

  getSelf(): Participant {
    this.participants.forEach(participantRelation => {
      if (participantRelation.relationship === UserParticipant.SELF_GUARDIAN ||
        participantRelation.relationship === UserParticipant.SELF_PARTICIPANT) {
        return (participantRelation.participant);
      }
    });
    return null;
  }

  getDependents() {
    return this.participants.filter(pr => { pr.relationship === 'dependent'; })
      .map(pr => pr.participant);
  }


}
