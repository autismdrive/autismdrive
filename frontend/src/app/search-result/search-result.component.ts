import {Component, Input, OnInit} from '@angular/core';
import {Hit} from '../_models/query';
import {LatLngLiteral} from '@agm/core';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit {
  @Input() hit: Hit;
  @Input() mapLoc: LatLngLiteral;

  hover = false;

  constructor() {
  }

  ngOnInit() {
  }

}
