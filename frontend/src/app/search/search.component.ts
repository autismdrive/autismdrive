import {
  Component,
  OnDestroy,
  OnInit,
  Renderer2,
  ViewChild
} from '@angular/core';
import { MatPaginator, MatSidenav } from '@angular/material';
import { ActivatedRoute, Router, Params, ParamMap } from '@angular/router';
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
    private searchService: SearchService
  ) {
    this.route.queryParamMap.subscribe(qParams => {
      let words = '';
      const filters: Filter[] = [];

      for (const key of qParams.keys) {
        if (key === 'words') {
          words = qParams.get(key);
        } else {
          filters.push({ field: key, value: qParams.getAll(key) });
        }
      }

      this.query = new Query({
        words: words,
        filters: filters,
        size: this.pageSize,
      });

      this.doSearch();
      this.updateFilters();
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
    if (this.paginator) {
      this.paginator.firstPage();
    }
    this.updateUrl(this.query);
  }

  updateUrl(query: Query) {
    const queryParams: Params = {};

    if (query.hasOwnProperty('words') && query.words) {
      queryParams.words = query.words;
    } else {
      queryParams.words = undefined;
    }

    for (const filter of query.filters) {
      queryParams[filter.field] = filter.value;
    }

    this.router.navigate(
      [],
      {
        relativeTo: this.route,
        queryParams: queryParams
      });
  }

  doSearch() {
    this.loading = true;
    this.searchService
      .search(this.query)
      .subscribe(queryWithResults => {
        if (this.query.equals(queryWithResults)) {
          this.query = queryWithResults;
          this.checkWindowWidth();
          this.loading = false;
        } else {
          this.updateUrl(this.query);
        }
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
    this.updateUrl(this.query);
  }

  sortByRelevance() {
    this.query.sort = '_score';
    this.showFilters = false;
    this.query.start = 0;
    this.updateUrl(this.query);
  }

  addFilter(field: string, fieldValue: string) {
    const i = this.query.filters.findIndex(f => f.field === field);

    // Filter has already been set
    if (i > -1) {

      // Make sure it's not a duplicate value
      const j = this.query.filters[i].value.findIndex(v => v === fieldValue);

      if (j === -1) {
        this.query.filters[i].value.push(fieldValue);
      }
    } else {
      this.query.filters.push({ field: field, value: [fieldValue] });
    }

    this.query.start = 0;

    if (this.paginator) {
      this.paginator.firstPage();
    }

    this.updateUrl(this.query);
  }

  removeFilter(field: string, fieldValue: string) {
    const i = this.query.filters.findIndex(f => f.field === field);

    if (i > -1) {
      const j = this.query.filters[i].value.findIndex(v => v === fieldValue);
      if (j > -1) {
        this.query.filters[i].value.splice(j, 1);
      }
    }
    this.query.start = 0;
    this.updateUrl(this.query);
  }

  updatePage() {
    this.query.size = this.paginator.pageSize;
    this.query.start = (this.paginator.pageIndex * this.paginator.pageSize) + 1;
    this.updateUrl(this.query);
  }

  // Show filters if all filters have been removed.
  updateFilters() {
    this.showFilters = this.query.filters.length === 0;
    if (this.showFilters && this.sideNav) {
      this.sideNav.open();
    }
  }
}
