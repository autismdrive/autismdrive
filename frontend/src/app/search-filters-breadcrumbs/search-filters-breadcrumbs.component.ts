import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Query} from '@models/query';

@Component({
  selector: 'app-search-filters-breadcrumbs',
  templateUrl: './search-filters-breadcrumbs.component.html',
  styleUrls: ['./search-filters-breadcrumbs.component.scss'],
})
export class SearchFiltersBreadcrumbsComponent {
  @Input() query: Query;
  @Input() restrictToMappedResults: boolean;
  @Input() ageLabels: {[key: string]: string};
  @Input() languageLabels: {[key: string]: string};
  @Input() typeLabels: {[key: string]: string};
  @Output() mappedResultsChipClicked = new EventEmitter<boolean>();
  @Output() keywordChipClicked = new EventEmitter();
  @Output() ageRangeChipClicked = new EventEmitter();
  @Output() languageChipClicked = new EventEmitter();
  @Output() typeChipClicked = new EventEmitter();
  @Output() categoryChipClicked = new EventEmitter();
  @Output() clearAllClicked = new EventEmitter();

  constructor() {}
}
