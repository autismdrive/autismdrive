import {NgForOf} from '@angular/common';
import {Component, EventEmitter, Input, Output} from '@angular/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {SortMethod} from '@models/sort_method';

@Component({
  standalone: true,
  selector: 'app-search-sort',
  templateUrl: './search-sort.component.html',
  styleUrls: ['./search-sort.component.scss'],
  imports: [MatFormFieldModule, MatSelectModule, NgForOf],
})
export class SearchSortComponent {
  @Input() selectedSort: SortMethod;
  @Input() sortMethods: Record<string, SortMethod>;
  @Output() sortMethodSelected = new EventEmitter<SortMethod>();

  get sortMethodsList() {
    return Object.values(this.sortMethods);
  }
}
