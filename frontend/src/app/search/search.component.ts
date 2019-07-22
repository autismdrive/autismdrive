import { LatLngLiteral } from '@agm/core';
import { MediaMatcher } from '@angular/cdk/layout';
import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  Renderer2,
  ViewChild
} from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSidenav } from '@angular/material/sidenav';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Filter, Query, Sort, Hit, HitLabel } from '../_models/query';
import { SearchService } from '../_services/api/search.service';
import { StudyStatus } from '../_models/study';
import {merge} from 'rxjs';
import {tap} from 'rxjs/operators';

interface SortMethod {
  name: string;
  label: string;
  sortQuery: Sort;
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, AfterViewInit, OnDestroy {
  query =  new Query({
    words: '',
    filters: [],
    size: 20,
  });
  showFilters = false;
  loading = true;
  hideResults = false;
  filters: Filter[];
  pageSize = 20;
  mapLoc: LatLngLiteral = {
    lat: 37.9864031,
    lng: -81.6645856
  };
  mobileQuery: MediaQueryList;
  private _mobileQueryListener: () => void;
  sortMethods: SortMethod[] = [
    {
      name: 'Relevance',
      label: 'Relevance',
      sortQuery: {
        field: '_score',
        order: 'desc',
      }
    },
    {
      name: 'Distance',
      label: 'Near me',
      sortQuery: {
        field: 'geo_point',
        latitude: this.mapLoc.lat,
        longitude: this.mapLoc.lng,
        order: 'asc',
        unit: 'mi'
      }
    },
    {
      name: 'Date',
      label: 'Recently Updated',
      sortQuery: {
        field: 'last_updated',
        order: 'desc'
      }
    },
  ];
  selectedSort: SortMethod;
  @ViewChild('sidenav', {static: true}) public sideNav: MatSidenav;
  @ViewChild('paginator', {static: true}) paginator: MatPaginator;
  featuredStudies: Hit[];

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    private route: ActivatedRoute,
    private router: Router,
    private renderer: Renderer2,
    private searchService: SearchService,
    private featuredSearchService: SearchService,
    media: MediaMatcher,
  ) {
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
    this.loadMapLocation(() => {
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

        this.sortBy(this.sortMethods[0]);
        this.updateFilters();
      });
    });

    this.renderer.listen(window, 'resize', (event) => {
      this.checkWindowWidth();
    });
  }

  ngOnInit() {
  }

  ngAfterViewInit() {
    merge(this.paginator.page).pipe(
      tap(() => this.doSearch())
    ).subscribe();
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

    this.sideNav.opened = this.showFilters && !this.mobileQuery.matches;
  }

  removeWords() {
    this.query.words = '';
    this.query.start = 0;
    if (this.paginator) {
      this.paginator.firstPage();
    } else {
      console.log('NO PAGINATOR?', this.paginator);
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
    }).then(() => {
      window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
      });
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
          this.searchFeaturedStudies();
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

  searchFeaturedStudies() {
    const query = new Query(this.query);
    query.replaceFilter('Type', HitLabel.STUDY);
    query.filters.push({field: 'Status', value: [StudyStatus.currently_enrolling]});
    this.featuredSearchService.search(query).subscribe(queryWithResults => {
      console.log('Featured studies queryWithResults', queryWithResults);
    });
  }

  loadMapLocation(callback: Function) {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        this.mapLoc = {
          lat: p.coords.latitude,
          lng: p.coords.longitude
        };
        callback();
      });
    } else {
      callback();
    }
  }

  sortBy(selectedSort: SortMethod) {
    this.loading = true;
    this.selectedSort = selectedSort;
    this.query.start = 0;
    this.query.sort = selectedSort.sortQuery;


    if (selectedSort.name === 'Distance') {
      this.loadMapLocation(() => {
        this.query.sort.latitude = this.mapLoc.lat;
        this.query.sort.longitude = this.mapLoc.lng;
        this.doSearch();
      });
    } else {
      this.doSearch();
    }
  }

  addFilter(field: string, fieldValue: string) {
    this.query.addFilter(field, fieldValue);
    this.query.start = 0;

    if (this.paginator) {
      this.paginator.firstPage();
    }

    this.updateUrl(this.query);
  }

  removeFilter(field: string, fieldValue: string) {
    this.query.removeFilter(field, fieldValue);
    this.query.start = 0;
    this.updateUrl(this.query);
  }

  updatePage() {
    if (this.paginator) {
      this.query.size = this.paginator.pageSize;
      this.query.start = (this.paginator.pageIndex * this.paginator.pageSize) + 1;
      this.updateUrl(this.query);
    }
  }

  // Show filters if all filters have been removed.
  updateFilters() {
    this.showFilters = this.query.filters.length === 0;
    if (!this.mobileQuery.matches && this.showFilters && this.sideNav) {
      this.sideNav.open();
    }
  }
}
