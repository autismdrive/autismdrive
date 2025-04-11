import {Component, Inject} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {AdminNote} from '@models/admin_note';
import {AdminNoteDisplayComponent} from '../admin-note-display/admin-note-display.component';

@Component({
  standalone: true,
  selector: 'app-admin-note-form',
  templateUrl: './admin-note-form.component.html',
  styleUrls: ['./admin-note-form.component.scss'],
  imports: [MatButtonModule, MatDialogModule, MatFormFieldModule, MatInputModule, ReactiveFormsModule, FormsModule],
})
export class AdminNoteFormComponent {
  constructor(
    public dialogRef: MatDialogRef<AdminNoteDisplayComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {adminNote: AdminNote},
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
