import { Component, OnInit, Input, Inject, OnChanges, SimpleChanges } from '@angular/core';
import { Participant } from '../_models/participant';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { ParticipantProfileComponent } from '../participant-profile/participant-profile.component';
import { ApiService } from '../_services/api/api.service';
import { ParticipantRelationship } from '../_models/participantRelationship';

export interface DialogData {
  participant: Participant;
}

@Component({
  selector: 'app-avatar-dialog',
  templateUrl: './avatar-dialog.component.html',
  styleUrls: ['./avatar-dialog.component.scss']
})
export class AvatarDialogComponent implements OnInit {
  avatarImages: string[] = [];
  avatarColors: string[] = [];
  selectedIcon: string;
  selectedColor: string;

  constructor(
    private api: ApiService,
    public dialogRef: MatDialogRef<ParticipantProfileComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {
    for (let i = 0; i < 104; i++) {
      this.avatarImages[i] = (i + 1).toLocaleString('en', { minimumIntegerDigits: 3 });
    }

    for (let i = 0; i < 16; i++) {
      this.avatarColors[i] = `hsl(${i * 16},100%,80%)`;
    }

    this.selectedIcon = this.data.participant.avatar_icon || '001';
    this.selectedColor = this.data.participant.avatar_color || `hsl(0,100%,80%)`;

    this.dialogRef.afterOpen().subscribe(() => {
      const imageEl = document.getElementsByClassName('avatar-image-active')[0] as HTMLElement;
      const colorEl = document.getElementsByClassName('color-swatch-active')[0] as HTMLElement;

      if (imageEl) {
        const x = imageEl.offsetLeft - imageEl.clientWidth * 1.25 - imageEl.parentElement.clientWidth;
        imageEl.parentElement.scrollTo({ left: x });
      }
      if (colorEl) {
        const x = colorEl.offsetLeft - colorEl.clientWidth * 3 - colorEl.parentElement.clientWidth;
        colorEl.parentElement.scrollTo({ left: x });
      }
    });
  }

  ngOnInit(): void {
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  getPrompt(): string {
    const isSelf = this.data.participant.relationship !== ParticipantRelationship.DEPENDENT;
    const subj = isSelf ? 'your' : `${this.data.participant.name || 'your child'}'s`;
    return `Choose ${subj} avatar`;
  }

  setColor(color: string) {
    this.selectedColor = color;
  }

  setImage(image: string) {
    this.selectedIcon = image;
  }

  isSelectedImage(avatarImage: string): boolean {
    if (this.selectedIcon) {
      return avatarImage === this.selectedIcon;
    } else {
      return avatarImage === this.data.participant.avatar_icon;
    }
  }

  isSelectedColor(avatarColor: string): boolean {
    if (this.selectedColor) {
      return avatarColor === this.selectedColor;
    } else {
      return avatarColor === this.data.participant.avatar_color;
    }
  }

  scroll($event: MouseEvent, className: string, direction: string) {
    const el = document.getElementsByClassName(className)[0];
    const row = document.getElementsByClassName(className + '-row')[0];
    const dir = direction === 'left' ? -1 : 1;
    const x = row.clientWidth * dir;
    el.scrollBy(x, 0);
  }

  onSubmit() {
    this.data.participant.avatar_color = this.selectedColor || this.data.participant.avatar_color;
    this.data.participant.avatar_icon = this.selectedIcon || this.data.participant.avatar_icon;
    this.api.updateParticipant(this.data.participant).subscribe(() => this.dialogRef.close());
  }
}
