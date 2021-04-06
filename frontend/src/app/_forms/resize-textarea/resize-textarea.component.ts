import {Component, OnInit, ViewChild} from '@angular/core';
import { FieldType } from '@ngx-formly/core';
import { MatInput } from '@angular/material/input';

@Component({
  selector: 'app-resize-textarea',
  template: `
    <textarea matInput
              [id]="id"
              [formControl]="formControl"
              [cols]="to.cols"
              [rows]="to.rows"
              [placeholder]="to.placeholder"
              [formlyAttributes]="field"
              [matTextareaAutosize]="true"
    >
    </textarea>
  `,

  styleUrls: ['./resize-textarea.component.scss']
})
export class ResizeTextareaComponent extends FieldType implements OnInit {
  @ViewChild(MatInput) formFieldControl: MatInput;
  ngOnInit(): void {
  }

}
