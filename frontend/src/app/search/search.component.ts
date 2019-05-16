import { Location } from '@angular/common';
import {
  Component,
  OnDestroy,
  OnInit,
  Renderer2,
  ViewChild
} from '@angular/core';
import { MatPaginator, MatSidenav } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { Filter, Query } from '../_models/query';
import { SearchService } from '../_services/api/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy {
  query: Query;
  showFilters = false;
  loading = true;
  hideResults = false;
  filters: Filter[];
  pageSize = 20;

  @ViewChild('sidenav') public sideNav: MatSidenav;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private renderer: Renderer2,
    private searchService: SearchService,
    private location: Location
  ) {
    this.route.queryParamMap.subscribe(qParams => {
      let words = '';
      const filters: Filter[] = [];

      for (const key of qParams.keys) {
        if (key === 'words') {
          words = qParams.get(key);
        } else {
          filters.push({ field: key, value: qParams.get(key) });
        }
      }

      this.query = new Query({
        words: words,
        filters: filters,
        size: this.pageSize,
      });

      this.doSearch();

      this.showFilters = qParams.keys.length === 0;
    });

    this.renderer.listen(window, 'resize', (event) => {
      this.checkWindowWidth();
    });
  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    this.searchService.reset();
  }

  private checkWindowWidth(): void {
    if (window.innerWidth > 768) {
      this.sideNav.mode = 'side';
    } else {
      this.sideNav.mode = 'over';
    }

    this.sideNav.opened = this.showFilters;
  }

  removeWords() {
    this.query.words = '';
    this.query.start = 0;
    this.paginator.firstPage();
    this.doSearch();
    this.updateFilters();
  }

  updateUrl(query: Query) {
    const queryArray: string[] = [];

    if (query.hasOwnProperty('words') && query.words) {
      queryArray.push(`words=${query.words}`);
    }

    for (const filter of query.filters) {
      queryArray.push(`${filter.field}=${filter.value}`);
    }

    const url = queryArray.length > 0 ? `/search/filter?${queryArray.join('&')}` : '/search';
    // this.location.go(url);
    this.router.navigateByUrl(url);
  }

  doSearch() {
    this.loading = true;
    this.updateUrl(this.query);
    this.searchService
      .search(this.query)
      .subscribe(query => {
        this.query = query;
        //
        // this.hideResults = (
        //   (this.query.words === '') &&
        //   (this.query.filters.length === 0)
        // );

        this.loading = false;

        this.checkWindowWidth();
      });
    if ((<any>window).gtag) {
      (<any>window).gtag('event', this.query.words, {
        'event_category': 'search'
      });
    }
  }

  sortByDate() {
    this.query.sort = '-last_updated';
    this.showFilters = false;
    this.query.start = 0;
    this.doSearch();
  }

  sortByRelevance() {
    this.query.sort = '_score';
    this.showFilters = false;
    this.query.start = 0;
    this.doSearch();
  }

  addFilter(field: string, value: string) {
    this.query.filters.push({ field: field, value: value });
    this.showFilters = false;
    this.query.start = 0;

    if (this.paginator) {
      this.paginator.firstPage();
    }

    this.doSearch();
  }

  removeFilter(filter: Filter) {
    const index = this.query.filters.indexOf(filter, 0);
    if (index > -1) {
      this.query.filters.splice(index, 1);
    }

    this.updateFilters();
    this.query.start = 0;
    this.doSearch();
  }

  updatePage() {
    this.query.size = this.paginator.pageSize;
    this.query.start = (this.paginator.pageIndex * this.paginator.pageSize) + 1;
    this.doSearch();
  }

  // Show filters if all filters have been removed.
  updateFilters() {
    this.showFilters = this.query.filters.length === 0;
    if (this.showFilters) {
      this.sideNav.open();
    }
  }
}
