import {Component, Input, OnInit} from '@angular/core';
import {AccordionItem} from '../_models/accordion-item';

@Component({
  selector: 'app-accordion',
  templateUrl: './accordion.component.html',
  styleUrls: ['./accordion.component.scss'],
})
export class AccordionComponent implements OnInit {
  @Input() item: AccordionItem;

  constructor() {}

  ngOnInit() {}
}
