import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatIcon} from '@angular/material/icon';
import {ContactItem} from '@models/contact_item';
import {FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-contact-item',
  templateUrl: './contact-item.component.html',
  styleUrls: ['./contact-item.component.scss'],
  imports: [CommonModule, FlexModule, MatIcon],
})
export class ContactItemComponent {
  @Input() contactItem: ContactItem;

  constructor() {}

  isNotEmpty(s: string) {
    const trimmed = (s || '').replace(/\s/g, '');
    return trimmed !== '';
  }
}
