import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {ActivatedRoute, Router} from '@angular/router';
import {LogoComponent} from '@app/logo/logo.component';
import {FlowName} from '@models/flow';
import {Participant} from '@models/participant';
import {ParticipantRelationship} from '@models/participantRelationship';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';

@Component({
  standalone: true,
  selector: 'app-terms',
  templateUrl: './terms.component.html',
  styleUrls: ['./terms.component.scss'],
  imports: [PdfJsViewerModule, LogoComponent, FlexModule, CommonModule, MatButtonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
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
      this.relationship = params['relationship'];
      if ('preview' in params) {
        this.preview = params['preview'];
      }
    });

    effect(() => {
      this.user = this.authenticationService.currentUser();
    });
  }

  goProfile($event) {
    $event.preventDefault();
    this.router.navigate(['profile']);
  }

  getFlow(relationship: ParticipantRelationship): FlowName {
    if (relationship === ParticipantRelationship.SELF_PARTICIPANT) {
      return FlowName.SELF_INTAKE;
    } else if (relationship === ParticipantRelationship.SELF_GUARDIAN) {
      return FlowName.GUARDIAN_INTAKE;
    } else if (relationship === ParticipantRelationship.DEPENDENT) {
      return FlowName.DEPENDENT_INTAKE;
    } else if (relationship === ParticipantRelationship.SELF_PROFESSIONAL) {
      return FlowName.PROFESSIONAL_INTAKE;
    } else if (relationship === ParticipantRelationship.SELF_INTERESTED) {
      return FlowName.PROFESSIONAL_INTAKE;
    } else {
      throw new Error(`Invalid participant relationship type: ${relationship}`);
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
      this.googleAnalyticsService?.flowStartEvent(flow);
      this.user.participants.push(participant);
      this.router.navigate(['flow', flow, participant.id]);
    });
  }
}
