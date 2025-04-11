import {NgClass, NgIf} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIcon} from '@angular/material/icon';
import {RouterModule} from '@angular/router';
import {AccordionItem} from '@models/accordion-item';

@Component({
  standalone: true,
  selector: 'app-accordion',
  templateUrl: './accordion.component.html',
  styleUrls: ['./accordion.component.scss'],
  imports: [MatExpansionModule, CommonModule, CommonModule, MatIcon, RouterModule],
})
export class AccordionComponent {
  @Input() item: AccordionItem;

  constructor() {}
}
