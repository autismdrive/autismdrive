import {Component, ViewChild, ViewContainerRef} from '@angular/core';
import {FieldWrapper} from '@ngx-formly/core';

@Component({
  selector: 'app-group-validation-wrapper',
  templateUrl: './group-validation-wrapper.component.html',
  styleUrls: ['./group-validation-wrapper.component.scss'],
})
export class GroupValidationWrapperComponent extends FieldWrapper {
  @ViewChild('fieldComponent', {read: ViewContainerRef, static: true}) fieldComponent: ViewContainerRef;
}
