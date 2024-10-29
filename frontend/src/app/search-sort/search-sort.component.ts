import {Component, EventEmitter, Input, Output} from '@angular/core';
import {SortMethod} from '@models/sort_method';

@Component({
  selector: 'app-search-sort',
  templateUrl: './search-sort.component.html',
  styleUrls: ['./search-sort.component.scss'],
})
export class SearchSortComponent {
  @Input() selectedSort: SortMethod;
  @Input() sortMethods: Record<string, SortMethod>;
  @Output() sortMethodSelected = new EventEmitter<SortMethod>();

  get sortMethodsList() {
    return Object.values(this.sortMethods);
  }
}
