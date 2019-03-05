import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';
import { ParticipantRelationship } from '../participantRelationship';
import { ProfileState } from '../profileState';
import { Router } from '@angular/router';
import { Participant } from '../participant';


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
      console.log('this.state', this.state);

      this.state = this.user.getState();

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
    this.addParticipantAndGoToFlow(ParticipantRelationship.SELF_PARTICIPANT, 'self_intake');
  }

  enrollGuardian($event) {
    $event.preventDefault();
    this.addParticipantAndGoToFlow(ParticipantRelationship.SELF_GUARDIAN, 'guardian_intake');
  }

  enrollDependent($event) {
    $event.preventDefault();
    this.addParticipantAndGoToFlow(ParticipantRelationship.DEPENDENT, 'dependent_intake');
  }

  addParticipantAndGoToFlow(relationship: string, flow: string) {
    this.loading = true;
    const newParticipant = new Participant({
      user_id: this.user.id,
      user: this.user,
      last_updated: new Date(),
      relationship: relationship
    });

    this.api.addParticipant(newParticipant).subscribe(participant => {
      console.log('Navigating to flow/', flow, '/', participant.id);
      this.router.navigate(['flow', flow,  participant.id]);
    });
  }
}
