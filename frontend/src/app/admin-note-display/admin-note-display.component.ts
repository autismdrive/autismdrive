import {DatePipe, NgForOf, NgIf} from '@angular/common';
import {Component, Input, OnInit} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatLineModule} from '@angular/material/core';
import {MatDialog} from '@angular/material/dialog';
import {MatTooltipModule} from '@angular/material/tooltip';
import {AdminNote} from '@models/admin_note';
import {Resource} from '@models/resource';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AdminNoteFormComponent} from '../admin-note-form/admin-note-form.component';

@Component({
  standalone: true,
  selector: 'app-admin-note-display',
  templateUrl: './admin-note-display.component.html',
  styleUrls: ['./admin-note-display.component.scss'],
  imports: [
    DatePipe,
    FlexModule,
    MatButtonModule,
    MatCardModule,
    MatLineModule,
    MatTooltipModule,
    NgForOf,
    NgIf,
  ],
})
export class AdminNoteDisplayComponent implements OnInit {
  @Input() currentUser: User;
  @Input() currentResource: Resource;
  notes: AdminNote[];

  constructor(
    private api: ApiService,
    public dialog: MatDialog,
  ) {}

  ngOnInit() {
    this.getNotes();
  }

  getNotes() {
    this.api.getResourceAdminNotes(this.currentResource.id).subscribe(notes => {
      this.notes = notes;
    });
  }

  openDialog(adminNote?: AdminNote): void {
    const dialogRef = this.dialog.open(AdminNoteFormComponent, {
      data: {
        adminNote: adminNote || {
          user_id: this.currentUser.id,
          resource_id: this.currentResource.id,
          note: '',
        },
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      if (adminNote) {
        adminNote.note = result;
        this.api.updateAdminNote(adminNote).subscribe(x => {
          this.getNotes();
        });
      } else if (result && !adminNote) {
        this.api
          .addAdminNote({
            user_id: this.currentUser.id,
            resource_id: this.currentResource.id,
            note: result,
          })
          .subscribe(x => {
            this.getNotes();
          });
      }
    });
  }

  deleteNote(note) {
    this.api.deleteAdminNote(note).subscribe(x => {
      this.getNotes();
    });
  }
}
