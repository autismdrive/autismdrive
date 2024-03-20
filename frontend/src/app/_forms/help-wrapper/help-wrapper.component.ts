import {Component, Input, ViewChild, ViewContainerRef} from '@angular/core';
import {FieldWrapper, FormlyTemplateOptions} from '@ngx-formly/core';

@Component({
  selector: 'app-help-wrapper',
  templateUrl: './help-wrapper.component.html',
  styleUrls: ['./help-wrapper.component.scss'],
})
export class HelpWrapperComponent extends FieldWrapper {
  @Input() to: FormlyTemplateOptions;
  @ViewChild('fieldComponent', {read: ViewContainerRef, static: true}) fieldComponent: ViewContainerRef;
}
