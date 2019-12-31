import {AfterContentInit, Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {RepeatSectionDialogData} from '../../_models/repeat_section_dialog_data';
import {clone} from '../../../util/clone';

@Component({
  selector: 'app-repeat-section-dialog',
  templateUrl: './repeat-section-dialog.component.html',
  styleUrls: ['./repeat-section-dialog.component.scss']
})
export class RepeatSectionDialogComponent implements AfterContentInit {
  disableSave: boolean;
  initialModel: any;

  constructor(
    public dialogRef: MatDialogRef<RepeatSectionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: RepeatSectionDialogData
  ) {
  }

  ngAfterContentInit(): void {
    this.initialModel = clone(this.data.model);
    this.updateDisableSave();
  }

  updateDisableSave() {
    this.disableSave = !this.noErrors();
  }

  noErrors(): boolean {
    return this.data.fields.every(f => {
      return f.formControl && f.formControl.valid;
    });
  }

  onNoClick(): void {
    // Reset data model to initial state
    Object.keys(this.initialModel).forEach(k => {
      this.data.model[k] = this.initialModel[k];
    });

    const isEmpty = Object.keys(this.data.model).length === 0 && this.data.model.constructor === Object;
    this.dialogRef.close(isEmpty ? undefined : this.data.model);
  }

  highlightRequiredFields() {
    this.data.fields.forEach(f => {
      f.fieldGroup.forEach(fg => {
        fg.formControl.updateValueAndValidity();
        fg.formControl.markAsDirty();
      });
    });

    this.updateDisableSave();
  }

  onSubmit(): void {
    if (this.noErrors()) {
      this.dialogRef.close(this.data);
    }
  }
}
