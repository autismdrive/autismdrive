import {AgmMap, LatLngBounds, LatLngLiteral, MapsAPILoader} from '@agm/core';
import {MediaMatcher} from '@angular/cdk/layout';
import {Location} from '@angular/common';
import {ChangeDetectorRef, Component, OnDestroy, OnInit, Renderer2, ViewChild, AfterViewInit} from '@angular/core';
import {MatExpansionPanel} from '@angular/material/expansion';
import {MatInput} from '@angular/material/input';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {MatTabChangeEvent, MatTabGroup} from '@angular/material/tabs';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {fromEvent} from 'rxjs';
import {filter, map, pairwise, share, throttleTime} from 'rxjs/operators';
import {AccordionItem} from '../_models/accordion-item';
import {Category} from '../_models/category';
import {AgeRange, HitType, Language} from '../_models/hit_type';
import {Hit, Query, Sort} from '../_models/query';
import {Resource} from '../_models/resource';
import {Direction} from '../_models/scroll';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/api/authentication-service';
import {SearchService} from '../_services/api/search.service';
import {GoogleAnalyticsService} from '../google-analytics.service';
import {Meta} from '@angular/platform-browser';
import {Study} from '../_models/study';
import createClone from 'rfdc';

declare var google: any;

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
export class SearchComponent implements OnInit, AfterViewInit, OnDestroy {
  query: Query;
  mapQuery: Query;
  resourceTypes = HitType.all_resources();
  selectedMapResource: Resource;
  selectedMapHit: Hit;
  selectedType: HitType = HitType.ALL_RESOURCES;
  selectedTypeTabIndex = 0;
  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  typeLabels = HitType.labels;
  ageOptions = [];
  languageOptions = [];
  loading = true;
  pageSize = 20;
  noLocation = true;
  storedZip: string;
  updatedZip: string;
  setLocOpen = false;
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
  mapZoomLevel: number;
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
      name: 'Date',
      label: 'Happening Soon',
      sortQuery: {
        field: 'date',
        order: 'asc'
      }
    },
    {
      name: 'Drafts',
      label: 'Drafts',
      sortQuery: {
        field: 'is_draft',
        order: 'desc'
      }
    },
  ];
  selectedSort: SortMethod = this.sortMethods[0];
  selectedPageStart = 0;
  pageEvent: PageEvent;
  paginatorElement: MatPaginator;
  panelElement: MatExpansionPanel;
  currentUser: User;
  highlightedStudy: Study;
  resourceGatherers: AccordionItem[] = [
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
      name: 'The Faison Center',
      shortName: 'Faison Center',
      description: 'The Faison School provides full-time day school programs for students ages 5 to 22 years.',
      image: '/assets/partners/faison_center.png',
      url: 'https://www.faisoncenter.org',
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
    {
      name: 'Virginia Institute of Autism',
      shortName: 'VIA',
      description: `
        The Virginia Institute of Autism is dedicated to helping people overcome the challenges of autism through innovative,
        evidence-based programs in education, outreach and adult services.
      `,
      image: '/assets/partners/via.png',
      url: 'https://www.viaschool.org/',
    },
  ];
  private _mobileQueryListener: () => void;
  restrictToMappedResults: boolean;
  private mapBounds: LatLngBounds;
  private scrollDirection: Direction;

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
    private api: ApiService,
    private meta: Meta,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this._mobileQueryListener = () => this._updateFilterPanelState();
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this.languageOptions = this.getOptions(Language.labels);
    this.ageOptions = this.getOptions(AgeRange.labels);

    // Using addEventListener causes page failures for older Sarafi / webkit / iPhone
    // this.mobileQuery.addEventListener('change', this._mobileQueryListener);
    // tslint:disable-next-line:deprecation
    this.mobileQuery.addListener(this._mobileQueryListener);
    window.addEventListener('resize', this._mobileQueryListener);
    this.meta.updateTag(
        { property: 'og:image', content: window.location.origin + '/assets/home/hero-parent-child.jpg' },
        `property='og:image'`);
    this.meta.updateTag(
      { property: 'og:image:secure_url', content: window.location.origin + '/assets/home/hero-parent-child.jpg' },
      `property='og:image:secure_url'`);
    this.meta.updateTag(
      { name: 'twitter:image', content: window.location.origin + '/assets/home/hero-parent-child.jpg' },
      `name='twitter:image'`);
  }

  @ViewChild(MatPaginator, {static: false})
  set paginator(value: MatPaginator) {
    this.paginatorElement = value;
  }

  @ViewChild(MatExpansionPanel, {static: false})
  set panel(value: MatExpansionPanel) {
    this.panelElement = value;
    this._updateFilterPanelState();
  }

  get showLocationButton(): boolean {
    const isLocation = this.selectedType && ['event', 'location'].includes(this.selectedType.name);
    const isDistanceSort = this.selectedSort && this.selectedSort.name === 'Distance';
    return (isLocation || isDistanceSort);
  }

  get showLocationForm(): boolean {
    return !this.noLocation && !this.setLocOpen;
  }

  ngOnInit() {
    this.route.queryParamMap.subscribe(qParams => {
      this.query = this._queryParamsToQuery(qParams);
      if (navigator.geolocation) {
        this.gpsEnabled = true;
      }
      this.loadMapLocation(() => {
        if (qParams.get('sort') && this.sortMethods.find(m => m.name === qParams.get('sort')) !== undefined) {
          this.reSort(qParams.get('sort'));
        } else {
          this.reSort(this.query.words.length > 0 ? 'Relevance' : 'Distance', true);
        }
      });
    });

  }

  ngAfterViewInit() {
    this.watchScrollEvents();
    this.paginatorElement.pageIndex = (this.selectedPageStart - 1) / this.pageSize;
  }

  ngOnDestroy(): void {
    this.searchService.reset();
    // removeEventListener fails on older versions of iOS / Safari / iPhone
    // this.mobileQuery.removeEventListener('change', this._mobileQueryListener);
    // tslint:disable-next-line:deprecation
    this.mobileQuery.removeListener(this._mobileQueryListener);
    window.removeEventListener('resize', this._mobileQueryListener);
  }

  getOptions(modelLabels) {
    const opts = [];
    for (const key in modelLabels) {
      if (modelLabels.hasOwnProperty(key)) {
        opts.push({'value': key, 'label': modelLabels[key]});
      }
    }
    return opts;
  }

  removeCategory() {
    this.query.category = null;
    this._goToFirstPage();
  }

  removeWords() {
    this.query.words = '';
    this._goToFirstPage();
  }

  updateUrlAndDoSearch() {
    const qParams = this._queryToQueryParams(this.query);
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: qParams,
    }).finally(() => {
      this.doSearch();
    });
  }

  scrollToTopOfSearch() {
    document.getElementById('TopOfSearch').scrollIntoView();
  }

  doSearch() {
    this.loading = true;
    const mapDataOnly = !this.restrictToMappedResults;
    this.searchService
      .mapSearch(this.query, mapDataOnly)
      .subscribe(mapQueryWithResults => {
        this.mapQuery = mapQueryWithResults;
        this.loadMapResults();
        this.loading = false;
      });
    this.searchService
      .search(this.query)
      .subscribe(queryWithResults => {
        this.query = queryWithResults;
        this.loading = false;
      });

    const studyQuery = createClone()(this.query);
    studyQuery.types = ['study'];
    this.api.searchStudies(studyQuery).subscribe(results => {
      if (results.hits.length > 0) {
        this.api.getStudy(results.hits[0].id).subscribe(study => {
          this.highlightedStudy = study;
        });
      } else {
        this.api.getStudiesByStatus('currently_enrolling').subscribe(studies => {
          this.highlightedStudy = studies[Math.floor(Math.random() * Math.floor(studies.length))];
        });
      }
    });
    this.googleAnalyticsService.searchEvent(this.query);
  }

  loadMapLocation(callback: Function) {
    this.storedZip = localStorage.getItem('zipCode');
    if (this.isZipCode(this.storedZip)) {
      this.api.getZipCoords(this.storedZip).subscribe(z => {
        this.noLocation = false;
        this.zipLoc = {
          lat: z.latitude,
          lng: z.longitude
        };
        this.mapLoc = this.zipLoc;
        callback.call(this);
      });
    } else {
      this.getGPSLocation(callback);
    }
  }

  getGPSLocation(callback: Function) {
    // If we already know the GPS location, then just return.
    if (this.gpsEnabled && this.gpsLoc) {
      this.noLocation = false;
      this.mapLoc = this.gpsLoc;
      callback.call(this);
      return;
    } else {
      this.noLocation = true;
      callback.call(this);
      // But don't return, go ahead and ask in the following chunk of code.
    }

    // Now, try to get the position, and if we can get it, use it.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        this.noLocation = false;
        this.gpsLoc = {
          lat: p.coords.latitude,
          lng: p.coords.longitude
        };
        this.mapLoc = this.gpsLoc;
        callback.call(this);
      }, error => {
        this.gpsEnabled = false;
        this.noLocation = true;
      });
    } else {
      this.noLocation = true;
      this.gpsEnabled = false;
    }
  }


  newSortSelection(sort: SortMethod) {
    this.loading = true;
    this.selectedSort = sort;
    this.updateUrlAndDoSearch();
  }

  reSort(sortName: string, forceReSort = false) {
    // Don't re-sort if it's already selected, but allow override.
    if ((sortName && (sortName !== this.selectedSort.name)) || forceReSort) {
      this.loading = true;
      this.selectedSort = this.sortMethods.find(s => s.name === sortName);
      this.query.start = this.selectedPageStart;
      this.selectedPageStart = 0;
      this.query.sort = this.selectedSort.sortQuery;

      if (this.selectedSort.name === 'Date') {
        this.selectType(HitType.EVENT.name);
      } else if (this.selectedSort.name === 'Distance') {
        this.loadMapLocation(() => this._updateDistanceSort());
      } else {
        this.updateUrlAndDoSearch();
      }
    }
  }

  selectAgeRange(age: string = null) {
    if (age) {
      this.query.ages = [age];
    } else {
      this.query.ages = [];
    }
    this._goToFirstPage();
  }

  selectLanguage(language: string = null) {
    if (language) {
      this.query.languages = [language];
    } else {
      this.query.languages = [];
    }
    this._goToFirstPage();
  }

  selectCategory(newCategory: Category) {
    this.query.category = newCategory;
    this._goToFirstPage();
  }

  selectType(keepType: string = null) {
    if (keepType) {
      this.selectedTypeTabIndex = this.resourceTypes.findIndex(t => t.name === keepType);
      this.selectedType = this.resourceTypes[this.selectedTypeTabIndex];

      if (keepType === HitType.ALL_RESOURCES.name) {
        this.query.types = this.resourceTypesFilteredNames();
      } else {
        this.query.types = [keepType];
      }
      this.query.date = keepType === HitType.EVENT.name ? new Date : undefined;

      if (keepType === HitType.LOCATION.name) {
        this.selectedSort = this.sortMethods.find(s => s.name === 'Distance');
      } else if (keepType === HitType.RESOURCE.name) {
        if (this.query.words !== '') {
          this.selectedSort = this.sortMethods.find(s => s.name === 'Relevance');
        } else {
          this.selectedSort = this.sortMethods.find(s => s.name === 'Updated');
        }
      } else if (keepType === HitType.EVENT.name) {
        this.selectedSort = this.sortMethods.find(s => s.name === 'Date');
      }
      this.query.sort = this.selectedSort.sortQuery;
    } else {
      this.selectedTypeTabIndex = this.resourceTypes.findIndex(t => t.name === HitType.ALL_RESOURCES.name);
      this.selectedType = this.resourceTypes[this.selectedTypeTabIndex];
      this.query.types = this.resourceTypesFilteredNames();
      this.query.date = null;
      this.reSort(this.query.words.length > 0 ? 'Relevance' : 'Distance');
    }
    this._goToFirstPage();
  }

  submitResource() {
    window.open('https://virginia.az1.qualtrics.com/jfe/form/SV_0JQAQjutv54EwnP', '_blank');
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
    this.updateUrlAndDoSearch();
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
      mapUI.setCenter(this.mapLoc || this.defaultLoc);
      mapUI.setZoom(9);
    });

    controlDiv.index = 1;
    mapUI.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  }

  showBreadcrumbs() {
    if (!this.query) {
      return false;
    }
    return this.query.hasFilters();
  }

  loadMapResults() {
    if (this.mapQuery && this.mapQuery.hits && (this.mapQuery.hits.length > 0)) {
      this.hitsWithAddress = this.mapQuery.hits.filter(h => !h.no_address);
      this.hitsWithNoAddress = this.mapQuery.hits.filter(h => h.no_address);
    } else {
      this.hitsWithAddress = [];
      this.hitsWithNoAddress = [];
    }
  }

  showMap() {
    const is_location_or_event_type = this.mapQuery &&
      this.mapQuery.types &&
      this.mapQuery.types.length === 1 &&
      (this.mapQuery.types.includes('location') ||
        this.mapQuery.types.includes('event'));
    const is_sort_by_distance = this.selectedSort.name === 'Distance';
    return is_location_or_event_type || is_sort_by_distance;
  }

  openSetLocation() {
    this.setLocOpen = true;
  }

  closeSetLocation() {
    this.setLocOpen = false;
  }

  zipSubmit($event: MouseEvent|KeyboardEvent, setLocationExpansionPanel: MatExpansionPanel): void {
    setLocationExpansionPanel.close();
    $event.stopPropagation();
    localStorage.setItem('zipCode', this.updatedZip || '');
    this.setLocOpen = false;
    this.reSort('Distance', true);
  }

  useGPSLocation($event: MouseEvent|KeyboardEvent, setLocationExpansionPanel: MatExpansionPanel): void {
    setLocationExpansionPanel.close();
    $event.stopPropagation();
    localStorage.removeItem('zipCode');
    this.storedZip = null;
    this.setLocOpen = false;
    this.reSort('Distance', true);
  }

  isZipCode(zipCode: string): boolean {
    return (zipCode && (zipCode !== '') && (/^\d{5}$/.test(zipCode)));
  }

  showInfoWindow(hit: Hit) {
    this.api.getResource(hit.id).subscribe(r => {
      this.selectedMapResource = r;
      this.selectedMapHit = hit;
      this.googleAnalyticsService.mapEvent(hit.id.toString());
    });
  }

  closeInfoWindow() {
    this.selectedMapResource = null;
    this.selectedMapHit = null;
  }

  isInfoWindowOpen(): boolean {
    return this.selectedMapResource != null;
  }

  // https://stackoverflow.com/a/19303725/1791917
  mapJitter(seed: number, isLat: boolean): number {
    let m = seed % 2 === 0 ? 1 : -1;
    if (isLat) {
      m = m * -1;
    }
    const x = Math.sin(seed) * 10000;
    return (x - Math.floor(x)) / 100 * m;
  }

  updateZoom(zoomLevel: number) {
    this.mapZoomLevel = zoomLevel;
  }

  getCircleRadius(): number {
    const maxMiles = 100;
    const metersPerMi = 1609.34;
    return maxMiles * metersPerMi / (this.mapZoomLevel || 1);
  }

  getMarkerIcon(hit: Hit) {
    const url = `/assets/map/${hit.type}${hit.no_address ? '-no-address' : ''}.svg`;
    const x = 16;
    const y = hit.no_address ? 16 : 0;
    return {url: url, anchor: {x: x, y: y}};
  }

  protected mapLoad(map: google.maps.Map) {
    this.addMyLocationControl(map);
  }

  private _queryToQueryParams(query: Query): Params {
    const queryParams: Params = {};

    if (query.hasOwnProperty('words') && query.words) {
      queryParams.words = query.words;
    } else {
      queryParams.words = undefined;
    }

    queryParams.types = query.types;
    queryParams.ages = query.ages;
    queryParams.languages = query.languages;
    queryParams.sort = this.selectedSort.name;
    queryParams.pageStart = query.start;

    if (query.hasOwnProperty('category') && query.category) {
      queryParams.category = query.category.id;
    }
    return queryParams;
  }

  get hits(): Hit[] {
    if (this.query && this.query.hits && this.query.hits.length > 0) {
      if (this.restrictToMappedResults) {
        return this.mapQuery.hits.filter(h => {
          if (h.hasCoords()) {
            const latLng = new google.maps.LatLng(h.latitude, h.longitude);
            return (this.mapBounds && this.mapBounds.contains(latLng));
          }
        });
      } else {
        return this.query.hits;
      }
    }

    return [];
  }

  // Return a random number for the given seed
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
            query.category = {'id': qParams.get(key)};
            break;
          case('ages'):
            query.ages = qParams.getAll(key);
            break;
          case('languages'):
            query.languages = qParams.getAll(key);
            break;
          case('sort'):
            if (this.sortMethods.find(m => m.name === qParams.get(key)) !== undefined) {
              query.sort = this.sortMethods.find(m => m.name === qParams.get(key)).sortQuery;
            }
            break;
          case('pageStart'):
            this.selectedPageStart = Number(qParams.get(key));
            break;
          case('types'):
            query.types = qParams.getAll(key);
        }
      }
    }
    return query;

  }

  private _updateDistanceSort() {
    const distance_sort = this.sortMethods.find(s => s.name === 'Distance');
    distance_sort.sortQuery.latitude = this.noLocation ? this.defaultLoc.lat : this.mapLoc.lat;
    distance_sort.sortQuery.longitude = this.noLocation ? this.defaultLoc.lng : this.mapLoc.lng;
    if (this.selectedSort.name === 'Distance') {
      this.selectedSort = distance_sort;
      this.query.sort = this.selectedSort.sortQuery;
      this.updateUrlAndDoSearch();
    }
  }

  private _goToFirstPage() {
    this.query.start = 0;
    if (this.paginatorElement) {
      this.paginatorElement.firstPage();
    }
    this.updateUrlAndDoSearch();
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

  selectTypeTab($event: MatTabChangeEvent) {
    const resourceType = ($event.index > 0) ? this.resourceTypesFiltered()[$event.index - 1] : HitType.ALL_RESOURCES;
    this.selectType(resourceType.name);
  }

  updateResultsList($event: LatLngBounds) {
    this.mapBounds = $event;
  }

  listMapResultsOnly(shouldRestrict: boolean) {
    this.restrictToMappedResults = shouldRestrict;
    this.updateUrlAndDoSearch();
  }

  isLastPage(): boolean {
    return (this.query.start + this.pageSize) < this.query.total;
  }

  numResultsFrom(): number {
    return (this.paginatorElement.pageIndex * this.pageSize) + 1;
  }

  numResultsTo(): number {
    return this.isLastPage() ? this.query.total : (this.paginatorElement.pageIndex + 1) * this.pageSize;
  }

  numTotalResults() {
    return this.query.total;
  }

  calculateMapHeight(mapContainer: HTMLDivElement) {
    return `${mapContainer.clientHeight}px`;
  }

  mapDockClass(scrollSpy: HTMLSpanElement, searchHeader: HTMLDivElement, searchFooter: HTMLDivElement): string {
    const scrollSpyPos = scrollSpy.getBoundingClientRect();
    const headerPos = searchHeader.getBoundingClientRect();
    const footerPos = searchFooter.getBoundingClientRect();
    const scrollDirection = this.scrollDirection ? this.scrollDirection.toLowerCase() : '';

    let alignClass = '';

    if (this._overlaps(scrollSpyPos, headerPos)) {
      alignClass = 'align-top';
    } else if (this._overlaps(scrollSpyPos, footerPos)) {
      alignClass = 'align-bottom';
    } else {
      alignClass = 'docked';
    }

    return alignClass + ' ' + scrollDirection;
  }

  private _overlaps(a: ClientRect | DOMRect, b: ClientRect | DOMRect): boolean {
    return (
      ((b.top < a.top) && (b.bottom > a.top)) ||      // b overlaps top edge of a
      ((b.top > a.top) && (b.bottom < a.bottom)) ||   // b inside a
      ((b.top < a.bottom) && (b.bottom > a.bottom))   // b overlaps bottom edge of a
    );
  }

  focusOnInput(zipCodeInput: HTMLInputElement) {
    zipCodeInput.focus();
  }

  watchScrollEvents() {
    const scroll$ = fromEvent(window, 'scroll').pipe(
      throttleTime(10),
      map((e: Event) => window.pageYOffset),
      pairwise(),
      map(([y1, y2]): Direction => (y2 < y1 ? Direction.Up : Direction.Down)),
      share()
    );

    scroll$
      .pipe(filter(direction => direction === Direction.Up))
      .subscribe(() => {
        this.scrollDirection = Direction.Up;
      });

    scroll$
      .pipe(filter(direction => direction === Direction.Down))
      .subscribe(() => {
        this.scrollDirection = Direction.Down;
      });
  }

}
