import {Component, Input} from '@angular/core';
import {ContactItem} from '@models/contact_item';

@Component({
  selector: 'app-contact-item',
  templateUrl: './contact-item.component.html',
  styleUrls: ['./contact-item.component.scss'],
})
export class ContactItemComponent {
  @Input() contactItem: ContactItem;

  constructor() {}

  isNotEmpty(s: string) {
    const trimmed = (s || '').replace(/\s/g, '');
    return trimmed !== '';
  }
}
