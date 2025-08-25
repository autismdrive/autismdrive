import {Component, Inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {StudyInvestigator} from '@models/study_investigator';
import {StudyDetailComponent} from '../study-detail/study-detail.component';

@Component({
  standalone: true,
  selector: 'app-investigator-form',
  templateUrl: './investigator-form.component.html',
  styleUrls: ['./investigator-form.component.scss'],
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, MatButtonModule, FormsModule],
})
export class InvestigatorFormComponent {
  constructor(
    public dialogRef: MatDialogRef<StudyDetailComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {si: StudyInvestigator},
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
