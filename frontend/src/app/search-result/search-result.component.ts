import { Component, OnInit, Input } from '@angular/core';
import { Hit } from '../_models/query';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit {
  @Input() hit: Hit;
  @Input() isFeatured: boolean;

  constructor() {
  }

  ngOnInit() {
  }

}
