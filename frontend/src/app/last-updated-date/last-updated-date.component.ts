import {DatePipe} from '@angular/common';
import {Component, Input} from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-last-updated-date',
  templateUrl: './last-updated-date.component.html',
  styleUrls: ['./last-updated-date.component.scss'],
  imports: [DatePipe],
})
export class LastUpdatedDateComponent {
  @Input() lastUpdatedDate: Date;

  constructor() {}
}
