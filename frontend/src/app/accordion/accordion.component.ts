import {Component, Input} from '@angular/core';
import {AccordionItem} from '@models/accordion-item';

@Component({
  selector: 'app-accordion',
  templateUrl: './accordion.component.html',
  styleUrls: ['./accordion.component.scss'],
})
export class AccordionComponent {
  @Input() item: AccordionItem;

  constructor() {}
}
