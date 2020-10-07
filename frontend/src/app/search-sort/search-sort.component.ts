import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {SortMethod} from '../_models/sort_method';

@Component({
  selector: 'app-search-sort',
  templateUrl: './search-sort.component.html',
  styleUrls: ['./search-sort.component.scss']
})
export class SearchSortComponent implements OnInit {
  @Input() selectedSort: SortMethod;
  @Input() sortMethods: SortMethod[];
  @Output() sortMethodSelected = new EventEmitter<SortMethod>();

  constructor() { }

  ngOnInit() {
  }

}
