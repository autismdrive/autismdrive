import {Component, Input, ViewChild, ViewContainerRef} from '@angular/core';
import {FieldWrapper, FormlyTemplateOptions} from '@ngx-formly/core';

@Component({
  selector: 'app-card-wrapper',
  templateUrl: './card-wrapper.component.html',
  styleUrls: ['./card-wrapper.component.scss'],
})
export class CardWrapperComponent extends FieldWrapper {
  @Input() to: FormlyTemplateOptions;
  @ViewChild('fieldComponent', {read: ViewContainerRef, static: true}) fieldComponent: ViewContainerRef;
}
