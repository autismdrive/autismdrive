import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { User } from '../_models/user';
import { ParticipantRelationship } from '../_models/participantRelationship';
import { Router } from '@angular/router';
import { Participant } from '../_models/participant';
import { Study } from '../_models/study';
import { StudyUser } from '../_models/study_user';
import { AuthenticationService } from '../_services/api/authentication-service';
import { Resource } from '../_models/resource';

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
  studyInquiries: StudyUser[];
  currentStudies: Study[];
  self: Participant;
  dependents: Participant[];
  favoriteResources: Resource[];
  selfPercentComplete: number;

  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router) {

    this.authenticationService.currentUser.subscribe(
      user => {
        this.user = user;
        this.self = user.getSelf();
        this.dependents = user.getDependents();
        this.state = this.getState();
        this.loading = false;
      }, error1 => {
        console.error(error1);
        this.user = null;
        this.loading = false;
      });
  }

  ngOnInit() {
    this.refreshParticipants();
    this.api.getUserStudyInquiries(this.user.id).subscribe( x => this.studyInquiries = x );
    this.api.getStudies().subscribe(all => {
      this.currentStudies = all.filter(s => s.status === 'currently_enrolling');
    });
    this.favoriteResources = this.user.user_favorites
      .filter(f => f.type === 'resource')
      .map(f => f.resource)
      .sort(a => a.id);
  }

  getFavoriteTopics(type) {
    return this.user.user_favorites.filter(f => f.type === type).map(f => f[type]);
  }

  refreshParticipants() {
    if (this.user) {
      this.api.getUser(this.user.id).subscribe( u => {
        const newU = new User(u);
        this.self = newU.getSelf();
        this.dependents = newU.getDependents();
        this.api.getFlow(newU.getSelf().getFlowName(), newU.getSelf().id).subscribe(
          f => {
            this.selfPercentComplete = f.percentComplete();
          }
        );
      });
    }
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
    this.router.navigate(['terms', ParticipantRelationship.SELF_PARTICIPANT]);
  }

  enrollGuardian($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.SELF_GUARDIAN]);
  }

  enrollDependent($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.DEPENDENT]);
  }

  enrollProfessional($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.SELF_PROFESSIONAL]);
  }
}
