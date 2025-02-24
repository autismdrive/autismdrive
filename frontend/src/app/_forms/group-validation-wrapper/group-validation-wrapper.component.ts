import {Component} from '@angular/core';
import {FieldWrapper, FormlyModule} from '@ngx-formly/core';

@Component({
  standalone: true,
  selector: 'app-group-validation-wrapper',
  templateUrl: './group-validation-wrapper.component.html',
  styleUrls: ['./group-validation-wrapper.component.scss'],
  imports: [FormlyModule],
})
export class GroupValidationWrapperComponent extends FieldWrapper {}
