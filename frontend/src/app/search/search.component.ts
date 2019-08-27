import {LatLngLiteral} from '@agm/core';
import {MediaMatcher} from '@angular/cdk/layout';
import {AfterViewInit, ChangeDetectorRef, Component, OnDestroy, OnInit, Renderer2, ViewChild} from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Filter, HitLabel, HitType, Query, Sort} from '../_models/query';
import {SearchService} from '../_services/api/search.service';
import {merge} from 'rxjs';
import {tap} from 'rxjs/operators';
import {GoogleAnalyticsService} from '../google-analytics.service';
import {scrollToTop} from '../../util/scrollToTop';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/api/authentication-service';
import {AccordionItem} from '../_models/accordion-item';

interface SortMethod {
  name: string;
  label: string;
  sortQuery: Sort;
}

interface ResourceType {
  name: string;
  label: string;
}

class MapControlDiv extends HTMLDivElement {
  index?: number;
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, AfterViewInit, OnDestroy {
  resourceTypes: ResourceType[] = ['RESOURCE', 'LOCATION', 'EVENT'].map(t => {
    return {name: HitType[t], label: HitLabel[t]};
  });
  query = new Query({
    words: '',
    filters: [],
    size: 20,
  });
  locQuery: Query;
  loading = true;
  hideResults = false;
  filters: Filter[];
  pageSize = 20;
  mapLoc: LatLngLiteral;

  defaultLoc: LatLngLiteral = {
    lat: 37.9864031,
    lng: -81.6645856
  };

  mobileQuery: MediaQueryList;
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
        latitude: this.mapLoc ? this.mapLoc.lat : this.defaultLoc.lat,
        longitude: this.mapLoc ? this.mapLoc.lng : this.defaultLoc.lng,
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
  @ViewChild('paginator', {static: true}) paginator: MatPaginator;
  currentUser: User;
  resourceGatherers: AccordionItem[] = [
    {
      name: 'Charlottesville Region Autism Action Group',
      shortName: 'CRAAG',
      description: `
        CRAAG is a parent-run advocacy group, one of three active all-volunteer regional Autism Action Groups
        initiated by Commonwealth Autism. Established in 2010, it serves Charlottesville, Albemarle, Greene,
        Fluvanna, Louisa, and Nelson counties.
      `,
      image: '/assets/partners/craag.png',
      url: 'https://cahumanservices.org/advocating-change/community-organization-engagement/autism-action-groups/',
    },
    {
      name: 'UVA Supporting Transformative Autism Research',
      shortName: 'UVA STAR',
      description: `
        The STAR initiative, led by the Curry School in partnership with colleagues across the University,
        aims to improve the lives of individuals with autism through groundbreaking research and innovative
        models for intervention and training.
      `,
      image: '/assets/partners/uva_star.png',
      url: 'https://curry.virginia.edu/faculty-research/centers-labs-projects/supporting-transformative-autism-research-star',
    },
    {
      name: 'Autism Speaks Inc.',
      shortName: 'Autism Speaks',
      description: `
        Autism Speaks Inc. is the largest autism advocacy organization in the United States. It sponsors autism research
        and conducts awareness and outreach activities aimed at families, governments, and the public.
      `,
      image: '/assets/partners/autism_speaks.png',
      url: 'https://www.autismspeaks.org/',
    }
  ];
  private readonly _mobileQueryListener: () => void;

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    private route: ActivatedRoute,
    private router: Router,
    private renderer: Renderer2,
    private searchService: SearchService,
    private locSearchService: SearchService,
    private featuredSearchService: SearchService,
    private googleAnalyticsService: GoogleAnalyticsService,
    private authenticationService: AuthenticationService,
    media: MediaMatcher,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);


    this.loadMapLocation(() => {
      this.loadLocResources();
      this.route.queryParamMap.subscribe(qParams => {
        let words = '';
        const filters: Filter[] = [];

        for (const key of qParams.keys) {
          if (key === 'words') {
            words = qParams.get(key);
          } else {
            filters.push({field: key, value: qParams.getAll(key)});
          }
        }

        this.query = new Query({
          words: words,
          filters: filters,
          size: this.pageSize,
        });

        this.sortBy(this.sortMethods[0]);
      });
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

  loadLocResources() {
    this.loading = true;

    this.locQuery = new Query({
      filters: [{field: 'Type', value: HitLabel.LOCATION}],
      start: 0,
      size: 999
    });
    if (this.mapLoc) {
      this.locQuery.sort = {
        field: 'geo_point',
        latitude: this.mapLoc.lat,
        longitude: this.mapLoc.lng,
        order: 'asc',
        unit: 'mi'
      };
    }

    this.locSearchService
      .search(this.locQuery)
      .subscribe(queryWithResults => {
        if (this.locQuery.equals(queryWithResults)) {
          this.locQuery = queryWithResults;
          this.loading = false;
        }
      });
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
      console.log('Done navigating to new route.', queryParams);
      scrollToTop();
    });
  }

  doSearch() {
    this.loading = true;
    this.searchService
      .search(this.query)
      .subscribe(queryWithResults => {
        if (this.query.equals(queryWithResults)) {
          this.query = queryWithResults;
          this.loading = false;
        } else {
          console.log('queryWithResults', queryWithResults);
          this.updateUrl(queryWithResults);
        }
      });
    this.googleAnalyticsService.event(this.query.words,
      {
        'event_category': 'search',
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

  selectResourceType(keepType: string) {
    this.resourceTypes.forEach(t => {
      if (t.label === keepType) {
        this.query.addFilter('Type', t.label);
      } else {
        this.query.removeFilter('Type', t.label);
      }
    });

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

  addMyLocationControl(mapUI: google.maps.Map) {
    const controlDiv: MapControlDiv = document.createElement('div');

    // Set CSS for the control border.
    const controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '6px';
    controlUI.style.marginRight = '12px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Your Location';
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    const controlText = document.createElement('div');
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = '<img src="/assets/map/my-location.svg">';
    controlUI.appendChild(controlText);

    // Set the center to the user's location on click
    controlUI.addEventListener('click', () => {
      this.loadMapLocation(() => {
        mapUI.setCenter(this.mapLoc);
        mapUI.setZoom(9);
      });
    });

    controlDiv.index = 1;
    mapUI.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  }

  addMapResources( mapUI: google.maps.Map) {
    if (this.locQuery) {
      console.log(this.locQuery.hits);
    }
  }

  protected mapLoad(map: google.maps.Map) {
    this.addMyLocationControl(map);
    this.addMapResources(map);
  }

  isSelectedResourceType(rt: ResourceType) {
    const types = this.query.filters.find(f => f.field === 'Type');

    if (types) {
      const f = types.value.find(t => {
        return t === rt.label;
      });

      if (f) {
        return true;
      }
    }
    return false;
  }
}
