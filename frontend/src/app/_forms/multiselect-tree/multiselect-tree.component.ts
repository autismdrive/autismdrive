import {Component, Input, OnInit, ViewChild, ViewContainerRef} from '@angular/core';
import {FieldWrapper, FormlyTemplateOptions} from '@ngx-formly/core';

@Component({
  selector: 'app-multiselect-tree',
  templateUrl: './multiselect-tree.component.html',
  styleUrls: ['./multiselect-tree.component.scss']
})
export class MultiselectTreeComponent extends FieldWrapper {
  @Input() to: FormlyTemplateOptions;
  @ViewChild('fieldComponent', { read: ViewContainerRef, static: true }) fieldComponent: ViewContainerRef;
}
