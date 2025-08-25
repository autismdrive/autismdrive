import {CommonModule, DatePipe} from '@angular/common';
import {Component, effect, Input, OnInit, signal, WritableSignal} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatLineModule} from '@angular/material/core';
import {MatDialog} from '@angular/material/dialog';
import {MatIconModule} from '@angular/material/icon';
import {MatTooltipModule} from '@angular/material/tooltip';
import {RouterModule} from '@angular/router';
import {AdminNote} from '@models/admin_note';
import {Resource} from '@models/resource';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {WindowService} from '@services/window/window.service';
import {firstValueFrom} from 'rxjs';
import {AdminNoteFormComponent} from '../admin-note-form/admin-note-form.component';

@Component({
  standalone: true,
  selector: 'app-admin-note-display',
  templateUrl: './admin-note-display.component.html',
  styleUrls: ['./admin-note-display.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    DatePipe,
    FlexModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatLineModule,
    MatTooltipModule,
  ],
})
export class AdminNoteDisplayComponent implements OnInit {
  @Input() currentUser: User;
  @Input() currentResource: Resource;
  notes: WritableSignal<AdminNote[]> = signal([]);
  resource: WritableSignal<Resource> = signal(null);

  constructor(
    private api: ApiService,
    public dialog: MatDialog,
    private windowService: WindowService,
  ) {
    // Update the resource when the given currentResource changes
    effect(async () => {
      if (this.currentResource?.id !== this.resource()?.id) this.resource.set(this.currentResource);
    });

    // Update the notes when the resource signal updates
    effect(async () => {
      if (this.resource()) await this.loadNotes();
    });
  }

  ngOnInit() {}

  async loadNotes() {
    const newNotes = await firstValueFrom(this.api.getResourceAdminNotes(this.currentResource.id));
    this.notes.set(newNotes);
  }

  async openDialog(adminNote?: AdminNote): Promise<void> {
    const dialogRef = this.dialog.open(AdminNoteFormComponent, {
      width: `${this.windowService.window.innerWidth}px`,
      autoFocus: '#save',
      data: {
        user_id: this.currentUser.id,
        resource_id: this.resource()?.id,
        note: '',
        ...adminNote,
      },
    });

    const result = await firstValueFrom(dialogRef.afterClosed());

    if (result === undefined) return; // Dialog was closed without action

    if (adminNote) {
      adminNote.note = result;
      await firstValueFrom(this.api.updateAdminNote(adminNote));
      await this.loadNotes();
    } else if (result && !adminNote) {
      await firstValueFrom(
        this.api.addAdminNote({
          user_id: this.currentUser.id,
          resource_id: this.currentResource.id,
          note: result,
        }),
      );
      await this.loadNotes();
    }
  }

  async deleteNote(note: AdminNote) {
    await firstValueFrom(this.api.deleteAdminNote(note));
    await this.loadNotes();
  }
}
