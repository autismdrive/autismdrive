import {NgForOf, NgIf} from '@angular/common';
import {Component, EventEmitter, Input, Output} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatChipsModule} from '@angular/material/chips';
import {MatIconModule} from '@angular/material/icon';
import {Query} from '@models/query';
import {ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-search-filters-breadcrumbs',
  templateUrl: './search-filters-breadcrumbs.component.html',
  styleUrls: ['./search-filters-breadcrumbs.component.scss'],
  imports: [ExtendedModule, FlexModule, MatChipsModule, MatIconModule, NgForOf, NgIf, MatButtonModule],
})
export class SearchFiltersBreadcrumbsComponent {
  @Input() query: Query;
  @Input() restrictToMappedResults: boolean;
  @Input() ageLabels: Record<string, string>;
  @Input() languageLabels: Record<string, string>;
  @Input() typeLabels: Record<string, string>;
  @Output() mappedResultsChipClicked = new EventEmitter<boolean>();
  @Output() keywordChipClicked = new EventEmitter();
  @Output() ageRangeChipClicked = new EventEmitter();
  @Output() languageChipClicked = new EventEmitter();
  @Output() typeChipClicked = new EventEmitter();
  @Output() categoryChipClicked = new EventEmitter();
  @Output() clearAllClicked = new EventEmitter();

  constructor() {}
}
