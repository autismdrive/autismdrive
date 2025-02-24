import {NgStyle, TitleCasePipe} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCard, MatCardModule} from '@angular/material/card';
import {MatDialog} from '@angular/material/dialog';
import {MatProgressBar, MatProgressBarModule} from '@angular/material/progress-bar';
import {Router} from '@angular/router';
import {Participant} from '@models/participant';
import {ParticipantRelationship} from '@models/participantRelationship';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AvatarDialogComponent} from '../avatar-dialog/avatar-dialog.component';

@Component({
  standalone: true,
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss'],
  imports: [MatCardModule, NgStyle, MatProgressBarModule, TitleCasePipe, FlexModule, MatButtonModule],
})
export class ParticipantProfileComponent {
  @Input() participant: Participant;
  @Input() user: User;

  constructor(
    private api: ApiService,
    private router: Router,
    public dialog: MatDialog,
  ) {}

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
    } else if (this.participant.relationship === ParticipantRelationship.SELF_INTERESTED) {
      $event.preventDefault();
      this.router.navigate(['flow', 'interested_intake', this.participant.id]);
    } else {
      $event.preventDefault();
      this.router.navigate(['flow', 'guardian_intake', this.participant.id]);
    }
  }

  goTerms($event) {
    $event.preventDefault();
    this.router.navigate(['terms', this.participant.relationship, {preview: true}]);
  }

  chooseAvatar($event, participant): void {
    const dialogRef = this.dialog.open(AvatarDialogComponent, {
      maxWidth: '100vw',
      maxHeight: '100vh',
      data: {participant: participant},
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
}
