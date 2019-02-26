import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';
import { Router } from '@angular/router';

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

  constructor(private api: ApiService, private router: Router) {
    this.api.getSession().subscribe(userProps => {
      this.user = new User(userProps);
      console.log('this.user', this.user);

      this.loading = false;
    }, error1 => {
      console.error(error1);
      this.user = null;
      this.loading = false;
    });
  }

  ngOnInit() {
  }

  enrollSelf($event) {
    $event.preventDefault();
    this.addParticipantAndGoToFlow(User.SELF_PARTICIPANT, 'self_intake');
  }

  enrollGuardian($event) {
    $event.preventDefault();
    this.addParticipantAndGoToFlow(User.SELF_GUARDIAN, 'guardian_intake');
  }

  enrollDependent($event) {
    $event.preventDefault();
    this.addParticipantAndGoToFlow(User.DEPENDENT, 'dependent_intake');
  }

  addParticipantAndGoToFlow(relationship: string, flow: string) {
    this.loading = true;
    const options = {
      user_id: this.user.id,
      user: this.user,
      last_updated: new Date(),
      relationship: relationship
    };

    this.api.addParticipant(options).subscribe(participant => {
      console.log('Navigating to participant/', participant.id, '/', flow);
      this.router.navigate(['participant', participant.id, flow]);
    });
  }
}
