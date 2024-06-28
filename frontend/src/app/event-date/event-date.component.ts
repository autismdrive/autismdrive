import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-event-date',
  templateUrl: './event-date.component.html',
  styleUrls: ['./event-date.component.scss'],
})
export class EventDateComponent {
  @Input() eventDate: Date;

  constructor() {}
}
