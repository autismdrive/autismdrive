import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';
import { Participant } from '../participant';
import { UserParticipant } from '../user-participant';

enum ProfileState {
  'NO_PARTICIPANT', 'PARTICIPANT', 'GUARDIAN'
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User;
  possibleStates = ProfileState;
  state = ProfileState.NO_PARTICIPANT;
  loading = true;
  userParticipants: UserParticipant[];
  currentId: number;

  constructor(private api: ApiService) {
    this.currentId = Math.floor(Math.random() * 99999999) + 999;
    this.api.getSession().subscribe(user => {
      this.user = user;
      this.userParticipants = user.participants;
      this.loading = false;
    }, error1 => {
      console.error(error1);
      this.user = null;
      this.loading = false;
    });
  }

  ngOnInit() {
  }

  /*
  addParticipant(relationship: string) {
    this.loading = true;
    const name = this.randomName();
    const options = new Participant({
      id: ++this.currentId,
      last_updated: new Date(),
      first_name: name.first,
      last_name: name.last,
      users: []
    });

    this.api.addParticipant(relationship, options).subscribe(participant => {
      this.api.getSession().subscribe(updatedUser => {
        this.user = updatedUser;
        this.userParticipants = updatedUser.participants;
        this.loading = false;
      });
    });
  }
*/
  isAlreadyEnrolled(relationship: string): boolean {
    for (const up of this.user.participants) {
      if (up.relationship === relationship) { return true; }
    }

    return false;
  }

}
