import {CommonModule} from '@angular/common';
import {AfterContentInit, Component, Inject} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {RepeatSectionDialogData} from '@app/shared/models/repeat_section_dialog_data';
import {clone} from '@app/shared/utilities/clone';
import {scrollToFirstInvalidField} from '@app/shared/utilities/scrollToTop';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {WindowService} from '@services/window/window.service';
import {DeviceDetectorService} from 'ngx-device-detector';

@Component({
  standalone: true,
  selector: 'app-repeat-section-dialog',
  templateUrl: './repeat-section-dialog.component.html',
  styleUrls: ['./repeat-section-dialog.component.scss'],
  imports: [FlexModule, MatButtonModule, FormlyModule, MatDialogModule, CommonModule],
})
export class RepeatSectionDialogComponent implements AfterContentInit {
  disableSave: boolean;
  initialModel: any;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: RepeatSectionDialogData,
    private deviceDetectorService: DeviceDetectorService,
    public dialogRef: MatDialogRef<RepeatSectionDialogComponent>,
    private windowService: WindowService,
  ) {}

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

  highlightRequiredFields(fields: FormlyFieldConfig[]) {
    fields.forEach(f => {
      f.formControl.updateValueAndValidity();
      f.formControl.markAsDirty();

      if (f.fieldGroup) {
        this.highlightRequiredFields(f.fieldGroup);
      }
    });

    this.updateDisableSave();
  }

  onInvalidFields(): void {
    this.highlightRequiredFields(this.data.fields);
    scrollToFirstInvalidField(this.deviceDetectorService, this.windowService);
  }

  onSubmit(): void {
    if (this.noErrors()) {
      this.dialogRef.close(this.data);
    }
  }
}
