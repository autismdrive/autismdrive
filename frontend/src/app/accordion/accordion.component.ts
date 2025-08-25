import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {RouterModule} from '@angular/router';
import {AccordionItem} from '@models/accordion-item';

@Component({
  standalone: true,
  selector: 'app-accordion',
  templateUrl: './accordion.component.html',
  styleUrls: ['./accordion.component.scss'],
  imports: [MatExpansionModule, CommonModule, MatIconModule, RouterModule],
})
export class AccordionComponent {
  @Input() item: AccordionItem;

  constructor() {}
}
