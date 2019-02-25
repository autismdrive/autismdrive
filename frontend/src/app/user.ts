import {Participant} from './participant';


export class User {

  static SELF_PARTICIPANT = 'self_participant';
  static SELF_GUARDIAN = 'self_guardian';
  static DEPENDENT = 'dependent';

  id: number;
  email: string;
  role: string;
  participants?: Participant[];
  last_updated?: Date;

  constructor(id: number, email: string, role: string) {
    this.id = id;
    this.email = email;
    this.role = role;
  }

  hasSelf() {
    return this.getSelf() !== null;
  }

  isSelf(participant: Participant): Boolean {
    if (participant.relationship === User.SELF_GUARDIAN ||
      participant.relationship === User.SELF_PARTICIPANT) {
      return true;
    } else {
      return false;
    }
  }

  getSelf(): Participant {
    this.participants.forEach(participant => {
      if (participant.relationship === User.SELF_GUARDIAN ||
        participant.relationship === User.SELF_PARTICIPANT) {
        return (participant);
      }
    });
    return null;
  }

  getDependents() {
    return this.participants.filter(pr => pr.relationship === User.DEPENDENT);
  }


}
