import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { User } from '../_models/user';
import { ParticipantRelationship } from '../_models/participantRelationship';
import { Router } from '@angular/router';
import { Participant } from '../_models/participant';
import {AuthenticationService} from '../_services/api/authentication-service';

enum ProfileState {
  NO_PARTICIPANT = 'NO_PARTICIPANT',
  PARTICIPANT = 'PARTICIPANT'
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

  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router) {

    this.authenticationService.refresh().subscribe(
      user => {
        this.user = user;
        this.state = this.getState();
        this.loading = false;
      }, error1 => {
        console.error(error1);
        this.user = null;
        this.loading = false;
      });
  }

  ngOnInit() {
  }

  getState() {
    if (!this.user) {  // can happen if user logs out from this page.
      return null;
    } else if (this.user.getSelf() === undefined) {
      return ProfileState.NO_PARTICIPANT;
    } else {
      return ProfileState.PARTICIPANT;
    }
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

  enrollProfessional($event) {
    $event.preventDefault();
    this.addParticipantAndGoToFlow(ParticipantRelationship.SELF_PROFESSIONAL, 'professional_intake');
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
