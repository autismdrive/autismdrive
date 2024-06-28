import {Component} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Participant} from '../_models/participant';
import {ParticipantRelationship} from '../_models/participantRelationship';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-terms',
  templateUrl: './terms.component.html',
  styleUrls: ['./terms.component.scss'],
})
export class TermsComponent {
  user: User;
  relationship: ParticipantRelationship;
  preview = false;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private authenticationService: AuthenticationService,
    private api: ApiService,
    private googleAnalyticsService: GoogleAnalyticsService,
  ) {
    this.route.params.subscribe(params => {
      this.relationship = params.relationship;
      if ('preview' in params) {
        this.preview = params['preview'];
      }
    });

    this.authenticationService.currentUser.subscribe(
      user => {
        this.user = user;
      },
      error1 => {
        console.error(error1);
        this.user = null;
      },
    );
  }

  goProfile($event) {
    $event.preventDefault();
    this.router.navigate(['profile']);
  }

  getFlow(relationship: ParticipantRelationship) {
    if (relationship === ParticipantRelationship.SELF_PARTICIPANT) {
      return 'self_intake';
    } else if (relationship === ParticipantRelationship.SELF_GUARDIAN) {
      return 'guardian_intake';
    } else if (relationship === ParticipantRelationship.DEPENDENT) {
      return 'dependent_intake';
    } else if (relationship === ParticipantRelationship.SELF_PROFESSIONAL) {
      return 'professional_intake';
    } else if (relationship === ParticipantRelationship.SELF_INTERESTED) {
      return 'interested_intake';
    }
  }

  addParticipantAndGoToFlow() {
    const newParticipant = new Participant({
      user_id: this.user.id,
      user: this.user,
      last_updated: new Date(),
      relationship: this.relationship,
      has_consented: true,
    });

    const flow = this.getFlow(this.relationship);

    this.api.addParticipant(newParticipant).subscribe(participant => {
      this.googleAnalyticsService.flowStartEvent(flow);
      this.user.participants.push(participant);
      console.log('Navigating to flow/', flow, '/', participant.id);
      this.router.navigate(['flow', flow, participant.id]);
    });
  }
}
