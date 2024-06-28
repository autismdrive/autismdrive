import {Component, OnInit, ViewChild} from '@angular/core';
import {MatInput} from '@angular/material/input';
import {FieldType} from '@ngx-formly/core';

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
export class ResizeTextareaComponent extends FieldType {
  @ViewChild(MatInput) formFieldControl: MatInput;
}
