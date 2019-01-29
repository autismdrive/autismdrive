import { Component } from '@angular/core';
import { FieldArrayType, FormlyFormBuilder } from '@ngx-formly/core';

@Component({
  selector: 'app-repeat-section',
  templateUrl: './repeat-section.component.html',
  styleUrls: ['./repeat-section.component.scss']
})
export class RepeatSectionComponent extends FieldArrayType {
  constructor(builder: FormlyFormBuilder) {
    super(builder);
  }
}
