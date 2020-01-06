import {Component, Input, OnInit} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {Router} from '@angular/router';
import {Participant} from '../_models/participant';
import {ParticipantRelationship} from '../_models/participantRelationship';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AvatarDialogComponent} from '../avatar-dialog/avatar-dialog.component';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() participant: Participant;
  @Input() user: User;

  constructor(
    private api: ApiService,
    private router: Router,
    public dialog: MatDialog
  ) {
  }

  ngOnInit() {
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

  goTerms($event) {
    $event.preventDefault();
    this.router.navigate(['terms', this.participant.relationship, {preview: true}]);
  }

  chooseAvatar($event, participant): void {
    const dialogRef = this.dialog.open(AvatarDialogComponent, {
      maxWidth: '100vw',
      maxHeight: '100vh',
      data: {participant: participant}
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
}
