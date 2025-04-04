import {NgForOf, NgIf} from '@angular/common';
import {Component, EventEmitter, Input, Output} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatHint} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatMenuModule} from '@angular/material/menu';
import {LoadingComponent} from '@app/loading/loading.component';
import {Aggregation} from '@models/query';

@Component({
  standalone: true,
  selector: 'app-search-filter',
  templateUrl: './search-filter.component.html',
  styleUrls: ['./search-filter.component.scss'],
  imports: [MatButtonModule, MatIconModule, MatMenuModule, MatHint, NgIf, LoadingComponent, NgForOf],
})
export class SearchFilterComponent {
  @Input() label_title: string;
  @Input() label_icon: string;
  @Input() label_any: string;
  @Input() label_map: {};
  @Input() aggregations: Aggregation[];
  @Input() isNotApplicable: boolean;
  @Input() notApplicableMessage: string;
  @Output() filterSelected = new EventEmitter<string>();

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
