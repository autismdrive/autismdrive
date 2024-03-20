import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-last-updated-date',
  templateUrl: './last-updated-date.component.html',
  styleUrls: ['./last-updated-date.component.scss'],
})
export class LastUpdatedDateComponent implements OnInit {
  @Input() lastUpdatedDate: Date;

  constructor() {}

  ngOnInit() {}
}
