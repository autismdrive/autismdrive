import {Component, Inject, OnInit} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {AdminNoteDisplayComponent} from '../admin-note-display/admin-note-display.component';
import {AdminNote} from '../_models/admin_note';

@Component({
  selector: 'app-admin-note-form',
  templateUrl: './admin-note-form.component.html',
  styleUrls: ['./admin-note-form.component.scss'],
})
export class AdminNoteFormComponent implements OnInit {
  constructor(
    public dialogRef: MatDialogRef<AdminNoteDisplayComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {adminNote: AdminNote},
  ) {}

  ngOnInit() {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
