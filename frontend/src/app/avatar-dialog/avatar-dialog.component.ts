import { Component, OnInit, Input, Inject } from '@angular/core';
import { Participant } from '../participant';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { ParticipantProfileComponent } from '../participant-profile/participant-profile.component';

export interface DialogData {
  participant: Participant;
}

@Component({
  selector: 'app-avatar-dialog',
  templateUrl: './avatar-dialog.component.html',
  styleUrls: ['./avatar-dialog.component.scss']
})
export class AvatarDialogComponent {
  avatarImages: string[] = [];
  avatarColors: string[] = [];

  constructor(public dialogRef: MatDialogRef<ParticipantProfileComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {

    for (let i = 0; i < 104; i++) {
      this.avatarImages[i] = i.toLocaleString('en', { minimumIntegerDigits: 3 });
    }

    for (let i = 0; i < 255; i = i + 16) {
      this.avatarColors[i] = `hsl(${i},100%,80%)`;
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
