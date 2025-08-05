import {CommonModule, DOCUMENT, NgOptimizedImage} from '@angular/common';
import {AfterViewInit, Component, Inject, signal, WritableSignal} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {MatIconModule} from '@angular/material/icon';
import {Participant} from '@models/participant';
import {ParticipantRelationship} from '@models/participantRelationship';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {lastValueFrom} from 'rxjs';
import {ParticipantProfileComponent} from '../participant-profile/participant-profile.component';

@Component({
  standalone: true,
  selector: 'app-avatar-dialog',
  templateUrl: './avatar-dialog.component.html',
  styleUrls: ['./avatar-dialog.component.scss'],
  imports: [MatDialogModule, FlexModule, CommonModule, MatButtonModule, MatIconModule, NgOptimizedImage],
})
export class AvatarDialogComponent implements AfterViewInit {
  avatarImages: WritableSignal<string[]> = signal([]);
  avatarColors: WritableSignal<string[]> = signal([]);
  selectedIcon: WritableSignal<string> = signal(undefined);
  selectedColor: WritableSignal<string> = signal(undefined);
  participant: WritableSignal<Participant> = signal(undefined);

  constructor(
    private api: ApiService,
    public dialogRef: MatDialogRef<ParticipantProfileComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {participant: Participant},
    @Inject(DOCUMENT) public document: Document,
  ) {
    this.avatarImages.set(
      Array(104)
        .fill(0)
        .map((_, i) => String(i + 1).padStart(3, '0')),
    );

    this.avatarColors.set(
      Array(16)
        .fill(0)
        .map((_, i) => `hsl(${i * 16},100%,80%)`),
    );

    this.selectedIcon.set(this.data.participant.avatar_icon || '001');
    this.selectedColor.set(this.data.participant.avatar_color || `hsl(0, 100%, 80%)`);
    this.participant.set(this.data.participant);
  }

  ngAfterViewInit() {
    const imageEl = this.document.getElementsByClassName('avatar-image-active')[0] as HTMLElement;
    const colorEl = this.document.getElementsByClassName('color-swatch-active')[0] as HTMLElement;

    if (imageEl) {
      const x = imageEl.offsetLeft - imageEl.clientWidth * 1.25 - imageEl.parentElement.clientWidth;
      imageEl.parentElement.scrollTo({left: x});
    }
    if (colorEl) {
      const x = colorEl.offsetLeft - colorEl.clientWidth * 3 - colorEl.parentElement.clientWidth;
      colorEl.parentElement.scrollTo({left: x});
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  get prompt(): string {
    const isSelf = this.data.participant.relationship !== ParticipantRelationship.DEPENDENT;
    const subj = isSelf ? 'your' : `${this.data.participant.name || 'your child'}'s`;
    return `Choose ${subj} avatar`;
  }

  scroll($event: MouseEvent, className: string, direction: string) {
    const el = document.getElementsByClassName(className)[0];
    const row = document.getElementsByClassName(className + '-row')[0];
    const dir = direction === 'left' ? -1 : 1;
    const x = row.clientWidth * dir;
    el.scrollBy(x, 0);
  }

  async onSubmit() {
    this.data.participant.avatar_color = this.selectedColor();
    this.data.participant.avatar_icon = this.selectedIcon();
    await lastValueFrom(this.api.updateParticipant(this.data.participant));
    this.dialogRef.close();
  }
}
