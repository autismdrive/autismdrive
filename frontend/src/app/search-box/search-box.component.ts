import { Component, OnInit, ViewChild } from '@angular/core';
import { MatInput } from '@angular/material';
import { Router } from '@angular/router';
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

  constructor(
    private router: Router,
    private searchService: SearchService
  ) {
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

  clearSearch() {
    this.words = '';

    if (this.isSearchPage()) {
      this.router.navigateByUrl('/search');
    }
  }

  updateSearch() {
    const value: string = this.searchInput && this.searchInput.value;

    if (value && (value.length > 0)) {
      this.router.navigateByUrl(`/search/filter?words=${value}`);
    } else {
      this.router.navigateByUrl('/search');
    }
  }

  hasWords(): boolean {
    return this.words && (this.words.length > 0);
  }

}
