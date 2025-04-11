import {DatePipe, NgIf} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-event-date',
  templateUrl: './event-date.component.html',
  styleUrls: ['./event-date.component.scss'],
  imports: [FlexModule, MatIconModule, DatePipe, NgIf],
})
export class EventDateComponent {
  @Input() eventDate: Date;

  constructor() {}
}
