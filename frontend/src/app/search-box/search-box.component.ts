import { Component, OnInit, ViewChild } from '@angular/core';
import { MatInput } from '@angular/material';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { SearchService } from '../_services/api/search.service';
import { debounce } from 'rxjs/operators';
import { timer } from 'rxjs';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.scss']
})
export class SearchBoxComponent implements OnInit {
  @ViewChild('searchInput', { read: MatInput }) public searchInput: MatInput;
  words = '';
  queryParams: Params;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService
  ) {
    this.route
      .queryParams
      .pipe(debounce(() => timer(1000)))
      .subscribe(qp => this.queryParams = qp);
    this.searchService
      .currentQuery
      .pipe(debounce(() => timer(1000)))
      .subscribe(q => this.words = (q && q.words) ? q.words : '');
  }

  ngOnInit() {
  }

  isSearchPage(): boolean {
    return (this.router.url.split('/')[1] === 'search');
  }

  showSearch() {
    if (this.searchInput) {
      this.searchInput.focus();
    }
  }

  updateSearch(removeWords: boolean) {
    if (removeWords) {
      this.words = '';
    }

    const newParams = JSON.parse(JSON.stringify(this.queryParams));
    const words: string = this.searchInput && this.searchInput.value || '';
    newParams.words = removeWords ? undefined : words;
    const hasFilters = Object.keys(newParams).length > 0;

    if (hasFilters) {
      this.router.navigate(['/search/filter'], { queryParams: newParams,  skipLocationChange: true });
    } else {
      this.router.navigateByUrl('/search');
    }
  }

  hasWords(): boolean {
    return this.words && (this.words.length > 0);
  }

}
