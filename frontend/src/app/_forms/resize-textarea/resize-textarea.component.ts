import {Component, ViewChild} from '@angular/core';
import {MatInput} from '@angular/material/input';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {FieldType} from '@ngx-formly/material';

@Component({
  selector: 'app-resize-textarea',
  template: `
    <textarea
      matInput
      [id]="id"
      [formControl]="formControl"
      [cols]="props.cols"
      [rows]="props.rows"
      [placeholder]="props.placeholder"
      [formlyAttributes]="field"
      [cdkTextareaAutosize]="true"
    >
    </textarea>
  `,

  styleUrls: ['./resize-textarea.component.scss'],
})
export class ResizeTextareaComponent extends FieldType<FormlyFieldConfig> {
  @ViewChild(MatInput) formFieldControl: MatInput;

  constructor() {
    super();
  }
}
