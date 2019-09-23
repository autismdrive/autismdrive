import {Component, Input, OnInit} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {AdminNoteFormComponent} from '../admin-note-form/admin-note-form.component';
import {ApiService} from '../_services/api/api.service';
import {AdminNote} from '../_models/admin_note';
import {Resource} from '../_models/resource';
import {User} from '../_models/user';

@Component({
  selector: 'app-admin-note-display',
  templateUrl: './admin-note-display.component.html',
  styleUrls: ['./admin-note-display.component.scss']
})
export class AdminNoteDisplayComponent implements OnInit {
  @Input() currentUser: User;
  @Input() currentResource: Resource;
  notes: AdminNote[];

  constructor(
    private api: ApiService,
    public dialog: MatDialog
  ) {

  }

  ngOnInit() {
    this.getNotes();
  }

  getNotes() {
    this.api.getResourceAdminNotes(this.currentResource.id).subscribe(notes =>{
      this.notes = notes;
    })
  }

  openDialog(adminNote): void {
    const dialogRef = this.dialog.open(AdminNoteFormComponent, {
      width: `${window.innerWidth / 2}px`,
      data: { adminNote: adminNote || {"user_id": this.currentUser.id, "resource_id": this.currentResource.id, "note": ''} }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (adminNote) {
        adminNote.note = result;
        this.api.updateAdminNote(adminNote).subscribe(x => {
          this.getNotes();
        });
      } else {
        this.api.addAdminNote({"user_id": this.currentUser.id, "resource_id": this.currentResource.id, "note": result}).subscribe(x => {
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
