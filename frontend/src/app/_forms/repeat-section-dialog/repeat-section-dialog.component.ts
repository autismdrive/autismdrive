import {AfterViewInit, Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {FormGroup} from '@angular/forms';
import {RepeatSectionDialogData} from '../../_models/repeat_section_dialog_data';

@Component({
  selector: 'app-repeat-section-dialog',
  templateUrl: './repeat-section-dialog.component.html',
  styleUrls: ['./repeat-section-dialog.component.scss']
})
export class RepeatSectionDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<RepeatSectionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: RepeatSectionDialogData
  ) {
    console.log('RepeatSectionDialogComponent constructor this.data', this.data);
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    this.dialogRef.close(this.data);
  }
}
