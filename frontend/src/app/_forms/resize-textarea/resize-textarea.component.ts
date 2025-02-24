import {CdkTextareaAutosize} from '@angular/cdk/text-field';
import {Component, ViewChild} from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {MatInput} from '@angular/material/input';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {FieldType} from '@ngx-formly/material';

@Component({
  standalone: true,
  selector: 'app-resize-textarea',
  templateUrl: './resize-textarea.component.html',
  styleUrls: ['./resize-textarea.component.scss'],
  imports: [ReactiveFormsModule, MatInput, FormlyModule, CdkTextareaAutosize],
})
export class ResizeTextareaComponent extends FieldType<FormlyFieldConfig> {
  @ViewChild(MatInput) formFieldControl: MatInput;

  constructor() {
    super();
  }
}
