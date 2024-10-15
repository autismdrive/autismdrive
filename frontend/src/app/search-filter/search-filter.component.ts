import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Aggregation} from '@models/query';

@Component({
  selector: 'app-search-filter',
  templateUrl: './search-filter.component.html',
  styleUrls: ['./search-filter.component.scss'],
})
export class SearchFilterComponent {
  @Input() label_title: string;
  @Input() label_icon: string;
  @Input() label_any: string;
  @Input() label_map: {};
  @Input() aggregations: Aggregation[];
  @Input() isNotApplicable: boolean;
  @Input() notApplicableMessage: string;
  @Output() filterSelected = new EventEmitter<String>();

  constructor() {}

  select(keepType?: string) {
    this.filterSelected.emit(keepType);
  }

  hasSelection(): boolean {
    return this.aggregations.filter(agg => agg.is_selected).length === 1;
  }

  selectedAgg(): Aggregation {
    if (this.hasSelection()) {
      return this.aggregations.filter(agg => agg.is_selected)[0];
    } else {
      // No selection. Return empty Aggregation.
      return {
        value: null,
        count: 0,
        is_selected: true,
      } as Aggregation;
    }
  }
}
