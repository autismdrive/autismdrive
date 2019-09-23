import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';import {AdminNote} from '../_models/admin_note';
import {AdminNoteDisplayComponent} from '../admin-note-display/admin-note-display.component';

@Component({
  selector: 'app-admin-note-form',
  templateUrl: './admin-note-form.component.html',
  styleUrls: ['./admin-note-form.component.scss']
})
export class AdminNoteFormComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<AdminNoteDisplayComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {adminNote: AdminNote}
    ) { }

  ngOnInit() {
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
