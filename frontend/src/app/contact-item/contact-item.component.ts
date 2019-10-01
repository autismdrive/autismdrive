import {Component, Input, OnInit} from '@angular/core';
import {ContactItem} from '../_models/contact_item';

@Component({
  selector: 'app-contact-item',
  templateUrl: './contact-item.component.html',
  styleUrls: ['./contact-item.component.scss']
})
export class ContactItemComponent implements OnInit {
  @Input() contactItem: ContactItem;

  constructor() {
  }

  ngOnInit() {
  }

  isNotEmpty(s: string) {
    const trimmed = (s || '').replace(/\s/g, '');
    return trimmed !== '';
  }

}
