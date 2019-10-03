import {AgmInfoWindow, LatLngLiteral} from '@agm/core';
import {MediaMatcher} from '@angular/cdk/layout';
import {ChangeDetectorRef, Component, OnDestroy, OnInit, Renderer2, ViewChild} from '@angular/core';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Location} from '@angular/common';
import {Hit, Query, Sort} from '../_models/query';
import {SearchService} from '../_services/api/search.service';
import {GoogleAnalyticsService} from '../google-analytics.service';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/api/authentication-service';
import {AccordionItem} from '../_models/accordion-item';
import {Category} from '../_models/category';
import {MatDialog} from '@angular/material/dialog';
import {SetLocationDialogComponent} from '../set-location-dialog/set-location-dialog.component';
import {ApiService} from '../_services/api/api.service';
import {AgeRange, HitType} from '../_models/hit_type';
import {MatExpansionPanel} from '@angular/material/expansion';

interface SortMethod {
  name: string;
  label: string;
  sortQuery: Sort;
}


class MapControlDiv extends HTMLDivElement {
  index?: number;
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit, OnDestroy {

  constructor(
    private changeDetectorRef: ChangeDetectorRef,
    private route: ActivatedRoute,
    private router: Router,
    private location: Location,
    private renderer: Renderer2,
    private searchService: SearchService,
    private googleAnalyticsService: GoogleAnalyticsService,
    private authenticationService: AuthenticationService,
    media: MediaMatcher,
    public locationDialog: MatDialog,
    private api: ApiService
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this._mobileQueryListener = () => this._updateFilterPanelState();
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this.mobileQuery.addEventListener('change', this._mobileQueryListener);
    window.addEventListener('resize', this._mobileQueryListener);

    this.loadMapLocation(() => {
      this.route.queryParamMap.subscribe(qParams => {
        this.query = this._queryParamsToQuery(qParams);
        this.loadMapResults();
        this.sortBy(this.query.words.length > 0 ? 'Relevance' : 'Distance');
      });
    });
  }

  query: Query;
  resourceTypes = HitType.all_resources();
  selectedType: HitType = HitType.ALL_RESOURCES;
  ageLabels = AgeRange.labels;
  typeLabels = HitType.labels;
  loading = true;
  pageSize = 20;
  noLocation = true;
  storedZip: string;
  gpsEnabled = false;
  zipLoc: LatLngLiteral;
  gpsLoc: LatLngLiteral;
  mapLoc: LatLngLiteral;
  defaultLoc: LatLngLiteral = {
    lat: 37.32248,
    lng: -78.36926
  };
  hitsWithNoAddress: Hit[] = [];
  hitsWithAddress: Hit[] = [];
  infoWindow: AgmInfoWindow;

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
      label: 'Distance from me',
      sortQuery: {
        field: 'geo_point',
        latitude: this.mapLoc ? this.mapLoc.lat : this.defaultLoc.lat,
        longitude: this.mapLoc ? this.mapLoc.lng : this.defaultLoc.lng,
        order: 'asc',
        unit: 'mi'
      }
    },
    {
      name: 'Updated',
      label: 'Recently Updated',
      sortQuery: {
        field: 'last_updated',
        order: 'desc'
      }
    },
    {
      name: 'Event Date',
      label: 'Happening Soon',
      sortQuery: {
        field: 'date',
        order: 'asc'
      }
    },
  ];
  selectedSort: SortMethod;

  pageEvent: PageEvent;
  paginatorElement: MatPaginator;
  @ViewChild(MatPaginator, {static: false})
  set paginator(value: MatPaginator) {
    this.paginatorElement = value;
  }

  panelElement: MatExpansionPanel;
  @ViewChild(MatExpansionPanel, {static: false})
  set panel(value: MatExpansionPanel) {
    this.panelElement = value;
    this._updateFilterPanelState();
  }

  currentUser: User;
  resourceGatherers: AccordionItem[] = [
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
      name: 'Charlottesville Region Autism Action Group',
      shortName: 'CRAAG',
      description: `
        A parent-run advocacy group, one of three active all-volunteer regional Autism Action Groups
        initiated by Commonwealth Autism. Established in 2010, it serves Charlottesville, Albemarle, Greene,
        Fluvanna, Louisa, and Nelson counties.
      `,
      image: '/assets/partners/craag.png',
      url: 'https://cahumanservices.org/advocating-change/community-organization-engagement/autism-action-groups/',
    },
    {
      name: 'Autism Speaks Inc.',
      shortName: 'Autism Speaks',
      description: `
        The largest autism advocacy organization in the United States. It sponsors autism research
        and conducts awareness and outreach activities aimed at families, governments, and the public.
      `,
      image: '/assets/partners/autism_speaks.png',
      url: 'https://www.autismspeaks.org/',
    },
    {
      name: 'Piedmont Regional Education Program',
      shortName: 'PREP',
      description: `
        A public regional organization designed to meet the needs of special education students. Provides special
        education programming and related services to nine school districts under an umbrella of a regional program.
      `,
      image: '/assets/partners/prep.png',
      url: 'http://www.prepivycreek.com/',
    },
  ];

  private _queryToQueryParams(query: Query): Params {
    const queryParams: Params = {};

    if (query.hasOwnProperty('words') && query.words) {
      queryParams.words = query.words;
    } else {
      queryParams.words = undefined;
    }

    queryParams.types = query.types;
    queryParams.ages = query.ages;

    if (query.hasOwnProperty('category') && query.category) {
      queryParams.category = query.category.id;
    }
    return queryParams;
  }

  private _queryParamsToQuery(qParams: Params): Query {

    const query = new Query({});
    query.size = this.pageSize;
    if (qParams && qParams.keys) {
      for (const key of qParams.keys) {
        switch (key) {
          case ('words'):
            query.words = qParams.get(key);
            break;
          case ('category'):
            query.category = {'id' : qParams.get(key)};
            break;
          case('ages'):
            query.ages = qParams.getAll(key);
            break;
          case('types'):
            query.types = qParams.getAll(key);
        }
      }
    }
    return query;
  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    this.searchService.reset();
    this.mobileQuery.removeEventListener('change', this._mobileQueryListener);
    window.removeEventListener('resize', this._mobileQueryListener);
  }

  removeCategory() {
    this.query.category = null;
    this._goToFirstPage(true);
  }

  removeWords() {
    this.query.words = '';
    this._goToFirstPage(true);
  }

  updateUrlAndDoSearch(query: Query) {
    const qParams = this._queryToQueryParams(query);
    const urlTree = this.router.parseUrl(this.router.url);
    const urlWithoutParams = urlTree.root.children['primary'].segments.map(it => it.path).join('/');

    this.location.go(
      this.router.createUrlTree(
        [urlWithoutParams],
        {queryParams: qParams}
      ).toString()
    );
    this.doSearch();
  }

  scrollToTopOfSearch() {
    document.getElementById('TopOfSearch').scrollIntoView();
  }

  doSearch() {
    this.loading = true;
    this.searchService
      .search(this.query)
      .subscribe(queryWithResults => {
        this.query = queryWithResults;
        this.loadMapResults();
        this.loading = false;
      });
    this.googleAnalyticsService.event(this.query.words,
      {
        'event_category': 'search',
      });
  }

  loadMapLocation(callback: Function) {
    let numStepsComplete = 0;
    const minStepsNeeded = 2;
    const _callCallbackIfReady = () => {
      numStepsComplete++;
      if (numStepsComplete >= minStepsNeeded) {
        this.mapLoc = this.zipLoc || this.gpsLoc;
        callback.call(this);
      }
    };

    this.storedZip = localStorage.getItem('zipCode');
    if (this.isZipCode(this.storedZip)) {
      this.api.getZipCoords(this.storedZip).subscribe(z => {
        this.noLocation = false;
        this.zipLoc = {
          lat: z.latitude,
          lng: z.longitude
        };
        _callCallbackIfReady();
      });
    } else {
      _callCallbackIfReady();
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        this.gpsEnabled = true;
        this.noLocation = false;

        this.gpsLoc = {
          lat: p.coords.latitude,
          lng: p.coords.longitude
        };

        _callCallbackIfReady();
      }, error => {
        this.gpsEnabled = false;
        _callCallbackIfReady();
      });
    } else {
      _callCallbackIfReady();
    }
  }

  isSortVisible(sort: SortMethod) {
    if (sort.name === 'Relevance' && this.query.words === '') {
      return false;
    } else {
      return true;
    }
  }

  isSortDisabled(sort: SortMethod) {
    if (sort.name === 'Relevance' && this.query.words === '') {
      return true;
    } else if (sort.name === 'Distance' && this.noLocation) {
      return true;
    } else {
      return false;
    }
  }

  sortBy(sortName: string) {
    this.loading = true;
    this.selectedSort = this.sortMethods.find(s => s.name === sortName);
    this.query.start = 0;
    this.query.sort = this.selectedSort.sortQuery;

    if (this.selectedSort.name === 'Event Date') {
      this.selectType(HitType.EVENT.name);
    } else if (this.selectedSort.name === 'Distance') {
      this.loadMapLocation(() => this._updateDistanceSort());
    } else {
      this.doSearch();
    }
  }

  selectAgeRange(age: string = null) {
    if (age) {
      this.query.ages = [age];
    } else {
      this.query.ages = [];
    }
    this._goToFirstPage(true);
  }

  selectCategory(newCategory: Category) {
    this.query.category = newCategory;
    this._goToFirstPage(true);
  }


  selectType(keepType: string = null) {
    if (keepType) {
      this.selectedType = this.resourceTypes.find(t => t.name === keepType);

      if (keepType === HitType.ALL_RESOURCES.name) {
        this.query.types = this.resourceTypesFilteredNames();
      } else {
        this.query.types = [keepType];
      }
      this.query.date = keepType === HitType.EVENT.name ? new Date : undefined;

      if (keepType === HitType.LOCATION.name) {
        this.selectedSort = this.sortMethods.filter(s => s.name === 'Distance')[0];
      } else if (keepType === HitType.RESOURCE.name) {
        if (this.query.words !== '') {
          this.selectedSort = this.sortMethods.filter(s => s.name === 'Relevance')[0];
        } else {
          this.selectedSort = this.sortMethods.filter(s => s.name === 'Updated')[0];
        }
      } else if (keepType === HitType.EVENT.name) {
        this.selectedSort = this.sortMethods.filter(s => s.name === 'Event Date')[0];
      }
    } else {
      this.selectedType = this.resourceTypes.find(t => t.name === HitType.ALL_RESOURCES.name);
      this.query.types = this.resourceTypesFilteredNames();
      this.query.date = null;
      this.sortBy(this.query.words.length > 0 ? 'Relevance' : 'Distance');
    }
    this._goToFirstPage(true);
  }

  resourceTypesFiltered(): HitType[] {
    return this.resourceTypes.filter(t => t.name !== HitType.ALL_RESOURCES.name);
  }

  resourceTypesFilteredNames(): string[] {
    return this.resourceTypesFiltered().map(t => t.name);
  }

  updatePage(event: PageEvent) {
    this.loading = true;
    this.pageEvent = event;
    this.query.size = event.pageSize;
    this.query.start = (event.pageIndex * event.pageSize) + 1;
    this.scrollToTopOfSearch();
    this.doSearch();
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
        mapUI.setCenter(this.mapLoc || this.defaultLoc);
        mapUI.setZoom(9);
      });
    });

    controlDiv.index = 1;
    mapUI.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  }

  protected mapLoad(map: google.maps.Map) {
    this.addMyLocationControl(map);
  }

  showBreadcrumbs() {
    if (!this.query) { return false; }
    return this.query.hasFilters();
  }

  loadMapResults() {
    if (this.query && this.query.hits && (this.query.hits.length > 0)) {
      const hitsWithCoords = this.query.hits.filter(h => h.hasCoords());

      if (hitsWithCoords && hitsWithCoords.length > 0) {
        this.hitsWithAddress = hitsWithCoords.filter(h => !h.no_address);
        this.hitsWithNoAddress = hitsWithCoords.filter(h => h.no_address);
      } else {
        this.hitsWithAddress = [];
        this.hitsWithNoAddress = [];
      }

    }
  }

  showMap() {
    const is_location_or_event_type = this.query &&
      this.query.types &&
      this.query.types.length === 1 &&
      (this.query.types.includes('location') ||
      this.query.types.includes('event'));
    const is_sort_by_distance = this.selectedSort && this.selectedSort.name === 'Distance';
    return is_location_or_event_type || is_sort_by_distance;
  }

  openLocationDialog() {
    const dialogRef = this.locationDialog.open(SetLocationDialogComponent, {
      width: '400px',
      data: {
        zipCode: localStorage.getItem('zipCode') || '',
        gpsEnabled: this.gpsEnabled
      }
    });

    dialogRef.afterClosed().subscribe(_ => {
      this.loadMapLocation(() => {
        if (this.mapLoc) {
          this.selectedSort = this.sortMethods.find(s => s.name === 'Distance');
        }

        this._updateDistanceSort();
      });
    });
  }

  isZipCode(zipCode: string): boolean {
    return (zipCode && (zipCode !== '') && (/^\d{5}$/.test(zipCode)));
  }

  private _updateDistanceSort() {
    const distance_sort = this.sortMethods.find(s => s.name === 'Distance');
    distance_sort.sortQuery.latitude = this.noLocation ? this.defaultLoc.lat : this.mapLoc.lat;
    distance_sort.sortQuery.longitude = this.noLocation ? this.defaultLoc.lng : this.mapLoc.lng;
    if (this.selectedSort.name === 'Distance') {
      this.selectedSort = distance_sort;
      this.query.sort = this.selectedSort.sortQuery;
      this.doSearch();
    }
  }

  private _goToFirstPage(shouldUpdateUrl = false) {
    this.query.start = 0;
    this.paginatorElement.firstPage();

    if (shouldUpdateUrl) {
      this.updateUrlAndDoSearch(this.query);
    } else {
      this.doSearch();
    }
  }

  private _updateFilterPanelState() {
    if (this.panelElement) {
      if (this.mobileQuery.matches) {
        this.panelElement.close();
        this.panelElement.hideToggle = false;
        this.panelElement.disabled = false;
      } else {
        this.panelElement.open();
        this.panelElement.hideToggle = true;
        this.panelElement.disabled = true;
      }
    }

    this.changeDetectorRef.detectChanges();
  }

  showInfoWindow(newInfoWindow) {
    if (this.infoWindow) {
      this.infoWindow.close().then(() => { this.infoWindow = newInfoWindow; });
    } else {
      this.infoWindow = newInfoWindow;
    }
  }

  closeInfoWindow() {
    if (this.infoWindow) {
      this.infoWindow.close();
    }
  }
}
