import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Participant } from '../_models/participant';
import { User } from '../_models/user';
import { ParticipantRelationship } from '../_models/participantRelationship';
import { Flow } from '../_models/flow';
import { ApiService } from '../_services/api/api.service';
import { AvatarDialogComponent } from '../avatar-dialog/avatar-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() participant: Participant;
  @Input() user: User;
  flow: Flow;
  percentComplete: number;
  numStudies: number;

  constructor(
    private api: ApiService,
    private router: Router,
    public dialog: MatDialog
  ) {
  }

  ngOnInit() {
    if (this.participant) {
      this.api
        .getFlow(this.participant.getFlowName(), this.participant.id)
        .subscribe(f => {
          this.flow = new Flow(f);
          console.log('this.flow', this.flow);
          this.percentComplete = this.flow.percentComplete();
          console.log('this.percentComplete', this.percentComplete);
        });
    }

    if (isFinite(this.participant.num_studies_enrolled)) {
      this.numStudies = this.participant.num_studies_enrolled;
    } else {
      this.numStudies = 0;
    }
  }

  goEditEnroll($event) {
    if (this.participant.relationship === ParticipantRelationship.SELF_PARTICIPANT) {
      $event.preventDefault();
      this.router.navigate(['flow', 'self_intake', this.participant.id]);
    } else if (this.participant.relationship === ParticipantRelationship.DEPENDENT) {
      $event.preventDefault();
      this.router.navigate(['flow', 'dependent_intake', this.participant.id]);
    } else if (this.participant.relationship === ParticipantRelationship.SELF_PROFESSIONAL) {
      $event.preventDefault();
      this.router.navigate(['flow', 'professional_intake', this.participant.id]);
    } else {
      $event.preventDefault();
      this.router.navigate(['flow', 'guardian_intake', this.participant.id]);
    }
  }

  chooseAvatar($event, participant): void {
    const dialogRef = this.dialog.open(AvatarDialogComponent, {
      width: `${window.innerWidth / 2}px`,
      data: { participant: participant }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
}
