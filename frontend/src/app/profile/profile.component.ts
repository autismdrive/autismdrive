import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';
import { Participant } from '../participant';
import {Router} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';

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
  currentId: number;

  constructor(private api: ApiService, private router: Router) {
    this.currentId = Math.floor(Math.random() * 99999999) + 999;
    this.api.getSession().subscribe(user => {
      this.user = user;
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


  addParticipantAndGoToFlow(relationship: string, flow: string) {
    this.loading = true;
    const options = {
      user_id: this.user.id,
      user: this.user,
      last_updated: new Date(),
      relationship: relationship
    };

    this.api.addParticipant(options).subscribe(participant => {
      console.log('Navigating to participant/', participant.id, '/', flow )
      this.router.navigate(['participant', participant.id, flow]);
    });
  }
}
