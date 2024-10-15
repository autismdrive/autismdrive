import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-last-updated-date',
  templateUrl: './last-updated-date.component.html',
  styleUrls: ['./last-updated-date.component.scss'],
})
export class LastUpdatedDateComponent {
  @Input() lastUpdatedDate: Date;

  constructor() {}
}
