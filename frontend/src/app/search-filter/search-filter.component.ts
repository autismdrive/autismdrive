import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Category} from '../_models/category';
import {Aggregation} from '../_models/query';

@Component({
  selector: 'app-search-filter',
  templateUrl: './search-filter.component.html',
  styleUrls: ['./search-filter.component.scss']
})
export class SearchFilterComponent implements OnInit {

  @Input() label_title: string;
  @Input() label_map: {};
  @Input() aggregations: Aggregation[];
  @Output() filterSelected = new EventEmitter<String>();

  constructor() { }

  ngOnInit() {
  }

  select(keepType: string) {
    this.filterSelected.emit(keepType);
  }

  hasSelection(): boolean {
    return this.aggregations.filter(agg => agg.is_selected).length === 1;
  }

  selectedAgg(): Aggregation {
    if (this.hasSelection()) {
      return this.aggregations.filter(agg => agg.is_selected)[0];
    }
  }
}
