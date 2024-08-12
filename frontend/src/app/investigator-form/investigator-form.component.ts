import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {StudyInvestigator} from '@models/study_investigator';
import {StudyDetailComponent} from '../study-detail/study-detail.component';

@Component({
  selector: 'app-investigator-form',
  templateUrl: './investigator-form.component.html',
  styleUrls: ['./investigator-form.component.scss'],
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
