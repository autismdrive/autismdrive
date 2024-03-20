import {Component, Inject, OnInit} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {StudyDetailComponent} from '../study-detail/study-detail.component';
import {StudyInvestigator} from '../_models/study_investigator';

@Component({
  selector: 'app-investigator-form',
  templateUrl: './investigator-form.component.html',
  styleUrls: ['./investigator-form.component.scss'],
})
export class InvestigatorFormComponent implements OnInit {
  constructor(
    public dialogRef: MatDialogRef<StudyDetailComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {si: StudyInvestigator},
  ) {}

  ngOnInit() {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
