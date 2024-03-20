import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-event-date',
  templateUrl: './event-date.component.html',
  styleUrls: ['./event-date.component.scss'],
})
export class EventDateComponent implements OnInit {
  @Input() eventDate: Date;

  constructor() {}

  ngOnInit() {}
}
