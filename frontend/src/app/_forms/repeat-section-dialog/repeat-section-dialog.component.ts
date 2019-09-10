import {AfterContentChecked, Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {RepeatSectionDialogData} from '../../_models/repeat_section_dialog_data';

@Component({
  selector: 'app-repeat-section-dialog',
  templateUrl: './repeat-section-dialog.component.html',
  styleUrls: ['./repeat-section-dialog.component.scss']
})
export class RepeatSectionDialogComponent implements AfterContentChecked {
  disableSave: boolean;

  constructor(
    public dialogRef: MatDialogRef<RepeatSectionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: RepeatSectionDialogData
  ) {
  }

  ngAfterContentChecked(): void {
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
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.noErrors()) {
      this.dialogRef.close(this.data);
    }
  }
}
