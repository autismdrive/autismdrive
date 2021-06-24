import {AgmMap, LatLngBounds} from '@agm/core';
import {animate, query, stagger, style, transition, trigger} from '@angular/animations';
import {Location} from '@angular/common';
import {AfterViewInit, ChangeDetectorRef, Component, HostBinding, OnDestroy, Renderer2, ViewChild} from '@angular/core';
import {MatExpansionPanel} from '@angular/material/expansion';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {MatTabChangeEvent} from '@angular/material/tabs';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, convertToParamMap, ParamMap, Params, Router} from '@angular/router';
import createClone from 'rfdc';
import {fromEvent} from 'rxjs';
import {filter, map, pairwise, share, throttleTime} from 'rxjs/operators';
import {AccordionItem} from '../_models/accordion-item';
import {Category} from '../_models/category';
import {AgeRange, HitType, Language} from '../_models/hit_type';
import {NavItem} from '../_models/nav-item';
import {Hit, Query} from '../_models/query';
import {Resource} from '../_models/resource';
import {Direction} from '../_models/scroll';
import {SortMethod} from '../_models/sort_method';
import {Study} from '../_models/study';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';
import {SearchService} from '../_services/search/search.service';
import LatLngLiteral = google.maps.LatLngLiteral;
import {getBounds} from 'geolib';


class MapControlDiv extends HTMLDivElement {
  index?: number;
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
  animations: [
    trigger('pageAnimations', [
      transition(':enter', [
        query('#age-filter, #language-filter, #topic-filter', [
          style({opacity: 0, transform: 'translateX(-100px)'}),
          stagger(-30, [
            animate('500ms cubic-bezier(0.35, 0, 0.25, 1)', style({opacity: 1, transform: 'none'}))
          ])
        ])
      ])
    ]),
  ]
})
export class SearchComponent implements AfterViewInit, OnDestroy {
  @HostBinding('@pageAnimations')
  public animatePage = true;
  query: Query;
  prevQuery: Query;
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
  pageSizeOptions = [20, 60, 100];
  pageSize = this.pageSizeOptions[0];
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
  defaultZoom: number = 7;
  mapZoomLevel: number;
  sortMethods: { [key: string]: SortMethod };
  selectedSort: SortMethod;
  paginatorElement: MatPaginator;
  mapTemplateElement: AgmMap;
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
  showFilters: boolean;
  expandResults: boolean;
  restrictToMappedResults: boolean;
  showDesignOptions = false;
  searchBgClasses = [
    'light-gray',
    'white',
    'uva-blue',
    'uva-orange',
    'black',
    'gray',
    'mountain',
    'sky',
    'energy-burst-dark',
    'energy-burst-light',
  ];
  searchBgClass = 'mountain';
  videoPlacement = 'right';
  videoSize = 'medium';
  videoId = 'oURTNCsiq3Y';
  videoInstructions = `Watch this video for tips about resources`;
  videoLinks: NavItem[] = [
    {
      label: 'Learn scientifically-supported interventions online',
      url: 'https://afirm.fpg.unc.edu/selecting-ebp',
    },
    {
      label: 'Read about scientifically-supported interventions',
      url: 'https://www.nationalautismcenter.org/resources/for-families/',
    },
    {
      label: 'Contact a Family Navigator for resource help',
      url: 'https://curry.virginia.edu/faculty-research/centers-labs-projects/star/resources/star-family-navigation',
    },
  ];
  expandTheme = false;
  queryParamMap: ParamMap;
  private mapBounds: LatLngBounds;
  private scrollDirection: Direction;

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private changeDetectorRef: ChangeDetectorRef,
    private googleAnalyticsService: GoogleAnalyticsService,
    private location: Location,
    private meta: Meta,
    private renderer: Renderer2,
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService,
  ) {
    this.sortMethods = {
      RELEVANCE: {
        name: 'Relevance',
        label: 'Relevance',
        sortQuery: {
          field: '_score',
          order: 'desc',
        }
      },
      DISTANCE: {
        name: 'Distance',
        label: 'Distance',
        sortQuery: {
          field: 'geo_point',
          latitude: this.mapLoc ? this.mapLoc.lat : this.defaultLoc.lat,
          longitude: this.mapLoc ? this.mapLoc.lng : this.defaultLoc.lng,
          order: 'asc',
          unit: 'mi'
        }
      },
      UPDATED: {
        name: 'Updated',
        label: 'Recently Updated',
        sortQuery: {
          field: 'last_updated',
          order: 'desc'
        }
      },
      DATE: {
        name: 'Date',
        label: 'Happening Soon',
        sortQuery: {
          field: 'date',
          order: 'asc'
        }
      },
      DRAFTS: {
        name: 'Drafts',
        label: 'Drafts',
        sortQuery: {
          field: 'is_draft',
          order: 'desc'
        }
      },
    };

    this.selectedSort = this.sortMethods.DISTANCE;
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.languageOptions = this.getOptions(Language.labels);
    this.ageOptions = this.getOptions(AgeRange.labels);

    this.meta.updateTag(
      {property: 'og:image', content: window.location.origin + '/assets/home/hero-parent-child.jpg'},
      `property='og:image'`);
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: window.location.origin + '/assets/home/hero-parent-child.jpg'},
      `property='og:image:secure_url'`);
    this.meta.updateTag(
      {name: 'twitter:image', content: window.location.origin + '/assets/home/hero-parent-child.jpg'},
      `name='twitter:image'`);

    this.loadMapLocation(() => {
      this.route.queryParamMap
        .subscribe(qParamMap => {
          this.queryParamMap = qParamMap;
          this.query = this._queryParamsToQuery(qParamMap);

          if (navigator.geolocation) {
            this.gpsEnabled = true;
          }
          this.mapZoomLevel = parseInt(qParamMap.get('zoom'), 10) || this.defaultZoom;
          // parse lat and lng from URL
          const qLat = qParamMap.get('lat');
          const qLng = qParamMap.get('lng');
          if (qLat && qLng) {
            this.mapLoc.lat = parseFloat(qLat);
            this.mapLoc.lng = parseFloat(qLng);
          } else {
            this.mapLoc.lat = this.defaultLoc.lat;
            this.mapLoc.lng = this.defaultLoc.lng;
          }
          const sortName = qParamMap.get('sort') || 'Distance';
          const forceReSort = (this.prevQuery && this.query.start === 0);

          if (forceReSort) {
            if (sortName && this.sortMethods[sortName.toUpperCase()]) {
              this.reSort(sortName, forceReSort);
            } else {
              this.reSort(this.query.hasWords ? 'Relevance' : 'Distance', forceReSort);
            }
          } else {
            this.selectedSort = this.sortMethods[sortName.toUpperCase()];
            this.doSearch();
          }
        });
    });

  }

  @ViewChild('paginator')
  set paginator(value: MatPaginator) {
    this.paginatorElement = value;
  }

  @ViewChild('mapTemplate')
  set mapTemplate(value: AgmMap) {
    this.mapTemplateElement = value;
  }

  get circleRadius(): number {
    const maxMiles = 100;
    const metersPerMi = 1609.34;
    return maxMiles * metersPerMi / (this.mapZoomLevel || 1);
  }

  get filtersPanelStyles() {
    const styles = {
      'full-screen': this.showFilters,
      'minimized': !this.showFilters,
    };

    styles[this.searchBgClass] = true;
    return styles;
  }

  get hits(): Hit[] {
    if (this.query && this.query.hasHits) {
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

  get isDistanceSort(): boolean {
    return (this.selectedSort && (this.selectedSort.name === 'Distance'));
  }

  get isInfoWindowOpen(): boolean {
    return this.selectedMapResource != null;
  }

  get isLastPage(): boolean {
    if (this.paginatorElement) {
      return !this.paginatorElement.hasNextPage();
    } else {
      return true;
    }
  }

  get numResultsFrom(): number {
    if (this.paginatorElement) {
      return (this.paginatorElement.pageIndex * this.pageSize) + 1;
    } else {
      return 0;
    }
  }

  get numResultsTo(): number {
    if (this.paginatorElement) {
      return this.isLastPage ? this.numTotalResults : (this.paginatorElement.pageIndex + 1) * this.pageSize;
    } else {
      return this.numTotalResults;
    }
  }

  get numTotalResults() {
    if (this.query && this.query.total) {
      return this.query.total;
    } else {
      return 0;
    }
  }

  get shouldHideVideo() {
    return !!localStorage.getItem('shouldHideTutorialVideo');
  }

  get showLocationButton(): boolean {
    const isLocation = this.selectedType && ['event', 'location'].includes(this.selectedType.name);
    return (isLocation || this.isDistanceSort);
  }

  get showLocationForm(): boolean {
    return !this.noLocation && !this.setLocOpen;
  }

  get shouldShowMap() {
    const is_location_or_event_type = this.mapQuery &&
      this.mapQuery.types &&
      this.mapQuery.types.length === 1 &&
      (this.mapQuery.types.includes('location') ||
        this.mapQuery.types.includes('event'));
    return is_location_or_event_type || this.isDistanceSort;
  }

  ngAfterViewInit() {
    this.watchScrollEvents();
  }

  ngOnDestroy(): void {
    this.searchService.reset();
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

  removeCategory(skipUpdate = false) {
    this.query.category = null;
    this._goToFirstPage(skipUpdate);
  }

  removeWords(skipUpdate = false) {
    this.query.words = '';
    this._goToFirstPage(skipUpdate);
  }

  scrollToTopOfSearch() {
    document.getElementById('TopOfSearch').scrollIntoView();
  }

  doSearch() {
    this.loading = true;
    console.log(this.query);
    if (this.query) {
      this._loadSearchResults();
      this._loadMapResults();
      this._loadRelatedStudies();
      this._updatePaginator();
    }
  }

  loadMapLocation(callback?: () => void) {
    this.storedZip = localStorage.getItem('zipCode');
    if (this.isZipCode(this.storedZip)) {
      this.api.getZipCoords(this.storedZip).subscribe(z => {
        console.log('this.api.getZipCoords subscribe callback');
        this.noLocation = false;
        this.zipLoc = {
          lat: z.latitude,
          lng: z.longitude
        };
        this.mapLoc = this.zipLoc;
        this._setDistanceSortLatLong();
        if (callback) { callback(); }
      });
    } else {
      this.getGPSLocation(callback);
    }
  }

  getGPSLocation(callback?: () => void) {
    // If we already know the GPS location, then just return.
    if (this.gpsEnabled && this.gpsLoc) {
      this.noLocation = false;
      this.mapLoc = this.gpsLoc;
      this._setDistanceSortLatLong();
      if (callback) { callback(); }
      return;
    } else {
      this.noLocation = true;
      // But don't return, go ahead and ask in the following chunk of code.
    }

    // Now, try to get the position, and if we can get it, use it.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        console.log('navigator.geolocation.getCurrentPosition callback');
        this.noLocation = false;
        this.gpsLoc = {
          lat: p.coords.latitude,
          lng: p.coords.longitude
        };
        this.mapLoc = this.gpsLoc;
        this._setDistanceSortLatLong();
        if (callback) { callback(); }
      }, error => {
        this.gpsEnabled = false;
        this.noLocation = true;
        this._setDistanceSortLatLong();
        if (callback) { callback(); }
    });
    } else {
      this.noLocation = true;
      this.gpsEnabled = false;
      this._setDistanceSortLatLong();
      if (callback) { callback(); }
    }
  }

  reSort(sortName: string, forceReSort = false) {
    console.log(`*** reSort sortName: ${sortName} ***`);
    // Don't re-sort if the query hasn't changed.
    const qParamsHaveChanged = this._queryParamsHaveChanged(this.queryParamMap);

    // Don't re-sort if it's already selected, but allow override.
    if ((qParamsHaveChanged && sortName && (sortName !== this.selectedSort.name)) || forceReSort) {
      this.loading = true;
      this.selectedSort = this.sortMethods[sortName.toUpperCase()];
      this.query.start = 0;
      this.query.sort = this.selectedSort.sortQuery;

      if (this.selectedSort.name === 'Date') {
        this.selectType(HitType.EVENT.name);
      } else if (this.isDistanceSort) {
        this._updateDistanceSort();
      } else {
        this.updateUrlAndDoSearch();
      }
    }
  }

  selectAgeRange(age: string = null, skipUpdate = false) {
    if (this.query && age) {
      this.query.ages = [age];
    } else {
      this.query.ages = [];
    }
    this._goToFirstPage(skipUpdate);
  }

  selectLanguage(language: string = null, skipUpdate = false) {
    if (language) {
      this.query.languages = [language];
    } else {
      this.query.languages = [];
    }
    this._goToFirstPage(skipUpdate);
  }

  selectCategory(newCategory: Category) {
    this.query.category = newCategory;
    this._goToFirstPage();
  }

  selectType(keepType: string = null, skipUpdate = false) {
    console.log(`=== selectType: keepType = ${keepType} ===`);
    const all = HitType.ALL_RESOURCES.name;
    const forceReSort = !(keepType && keepType !== all);

    if (forceReSort) {
      this.selectedTypeTabIndex = this.resourceTypes.findIndex(t => t.name === all);
      this.selectedType = this.resourceTypes[this.selectedTypeTabIndex];
      this.query.types = this.resourceTypesFilteredNames();
      this.query.date = null;
      this.selectedSort = this.sortMethods.DISTANCE;
    } else {
      this.selectedTypeTabIndex = this.resourceTypes.findIndex(t => t.name === keepType);
      this.selectedType = this.resourceTypes[this.selectedTypeTabIndex];
      this.query.types = (keepType === all) ? this.resourceTypesFilteredNames() : [keepType];
      this.query.date = keepType === HitType.EVENT.name ? new Date : undefined;

      if (keepType === HitType.LOCATION.name) {
        this.selectedSort = this.sortMethods.DISTANCE;
      } else if (keepType === HitType.RESOURCE.name) {
        if (this.query.hasWords) {
          this.selectedSort = this.sortMethods.RELEVANCE;
        } else {
          this.selectedSort = this.sortMethods.UPDATED;
        }
      } else if (keepType === HitType.EVENT.name) {
        this.selectedSort = this.sortMethods.DATE;
      }
      this.query.sort = this.selectedSort.sortQuery;
    }

    this._goToFirstPage(skipUpdate);
    this.reSort(this.selectedSort.name, forceReSort);
  }

  submitResource() {
    window.open('https://virginia.az1.qualtrics.com/jfe/form/SV_0JQAQjutv54EwnP', '_blank');
  }

  get resourceTypesFiltered(): HitType[] {
    return this.resourceTypes.filter(t => t.name !== HitType.ALL_RESOURCES.name);
  }

  resourceTypesFilteredNames(): string[] {
    return this.resourceTypesFiltered.map(t => t.name);
  }

  updatePage(event: PageEvent) {
    this.loading = true;
    this.query.size = event.pageSize;
    this.pageSize = event.pageSize;
    this.query.start = (event.pageIndex * event.pageSize) + 1;
    this.query.sort = this.selectedSort.sortQuery;
    console.log('here: ', this.query);
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
      this.loadMapLocation( () => {
        mapUI.setCenter(this.mapLoc || this.defaultLoc);
        mapUI.setZoom(9);
        this.updateUrlAndDoSearch();
      });
    });

    controlDiv.index = 1;
    mapUI.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  }

  showBreadcrumbs(): boolean {
    return !!(this.query && this.query.hasFilters);
  }

  openSetLocation() {
    this.setLocOpen = true;
  }

  closeSetLocation() {
    this.setLocOpen = false;
  }

  submitZip($event: MouseEvent | KeyboardEvent, setLocationExpansionPanel: MatExpansionPanel): void {
    setLocationExpansionPanel.close();
    $event.stopPropagation();
    localStorage.setItem('zipCode', this.updatedZip || '');
    this.googleAnalyticsService.searchInteractionEvent('set_zip_code_location');
    this.setLocOpen = false;
    this.loadMapLocation(() => {
      this.reSort('Distance', true);
    });
    this.mapZoomLevel = this.defaultZoom;
  }

  useGPSLocation($event: MouseEvent | KeyboardEvent, setLocationExpansionPanel: MatExpansionPanel): void {
    setLocationExpansionPanel.close();
    $event.stopPropagation();
    localStorage.removeItem('zipCode');
    this.googleAnalyticsService.searchInteractionEvent('set_gps_location');
    this.storedZip = null;
    this.setLocOpen = false;
    this.loadMapLocation();
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

  /**
   * Returns a random number for the given seed
   * https://stackoverflow.com/a/19303725/1791917
   **/
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
    this.updateUrlAndDoSearch();
  }

  getMarkerIcon(hit: Hit) {
    const url = `/assets/map/${hit.type}${hit.no_address ? '-no-address' : ''}.svg`;
    const x = 16;
    const y = hit.no_address ? 16 : 0;
    return {url: url, anchor: {x: x, y: y}};
  }

  selectTypeTab($event: MatTabChangeEvent) {
    const resourceType = ($event.index > 0) ? this.resourceTypesFiltered[$event.index - 1] : HitType.ALL_RESOURCES;
    this.selectType(resourceType.name);
  }

  updateResultsList($event: LatLngBounds) {
    this.mapBounds = $event;
  }

  listMapResultsOnly(shouldRestrict: boolean, skipUpdate = false) {
    this.restrictToMappedResults = shouldRestrict;
    if (shouldRestrict) {
      this.googleAnalyticsService.searchInteractionEvent('search_as_map_moves');
    }

    if (!skipUpdate) {
      this.updateUrlAndDoSearch();
    }
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

  clearAllFilters() {
    const skipUpdate = true;
    this.listMapResultsOnly(false, skipUpdate);
    this.removeWords(skipUpdate);
    this.selectAgeRange(null, skipUpdate);
    this.selectLanguage(null, skipUpdate);
    this.selectType(null, skipUpdate);
    this.removeCategory(skipUpdate);
    this.updateUrlAndDoSearch();
  }

  toggleShowFilters() {
    this.showFilters = !this.showFilters;

    if (!this.shouldShowMap) {
      this.expandResults = true;
    }
  }

  goSelectedMapResource(selectedMapResource: Resource) {
    this.googleAnalyticsService.mapResourceEvent(selectedMapResource.id.toString());
    this.router.navigate(['/' + selectedMapResource.type.toLowerCase() + '/' + selectedMapResource.id]);
  }

  hideVideo(shouldHide = true) {
    if (shouldHide) {
      localStorage.setItem('shouldHideTutorialVideo', `${shouldHide}`);
    } else {
      localStorage.removeItem('shouldHideTutorialVideo');
    }
  }

  showVideo(className: string) {
    this.videoPlacement = className;
    this.hideVideo(false);
  }

  updateUrlAndDoSearch() {
    const qParams = this._queryToQueryParams(this.query);

    const urlTree = this.router.createUrlTree([], {
      queryParams: qParams,
      queryParamsHandling: 'merge',
      preserveFragment: true
    });
    this.location.go(urlTree.toString());
       this.prevQuery = createClone()(this.query);
       this.doSearch();
       this.changeDetectorRef.detectChanges();
  }

  protected mapLoad(m: google.maps.Map) {
    this.addMyLocationControl(m);
    m.addListener('dragend', () => {
      this.onMapDrag();
    });
  }

  private _queryToQueryParams(qBefore: Query): Params {
    const q = createClone({circles: true})(qBefore);
    const queryParams: Params = {};

    if (q.hasOwnProperty('words') && q.words) {
      queryParams.words = q.words;
    }

    queryParams.types = q.types;
    queryParams.ages = q.ages;
    queryParams.languages = q.languages;
    queryParams.sort = queryParams.words ? this.sortMethods.RELEVANCE.name : this.selectedSort.name;
    queryParams.pageStart = q.start || 0;
    queryParams.zoom = this.mapZoomLevel;
    queryParams.lat = this.mapLoc.lat; // ? this.mapLoc.lat : this.defaultLoc.lat;
    queryParams.lng = this.mapLoc.lng; // ? this.mapLoc.lng : this.defaultLoc.lng;
    queryParams.geo_box = `${this.mapBounds.getNorthEast().lat()}|${this.mapBounds.getSouthWest().lng()}|${this.mapBounds.getSouthWest().lat()}|${this.mapBounds.getNorthEast().lng()}`;

    if (q.hasOwnProperty('category') && q.category) {
      queryParams.category = q.category.id;
    }
    return queryParams;
  }

  private _queryParamsToQuery(qParams: ParamMap): Query {
    const q = new Query({
      geo_box: undefined,
      words: '',
      ages: [],
      languages: [],
      sort: this.sortMethods.DISTANCE.sortQuery,
      start: 0,
      types: this.resourceTypesFilteredNames()
    });
    q.size = this.pageSize;
    if (qParams) {
      if (qParams.keys) {
        for (const key of qParams.keys) {
          if (qParams.get(key) !== undefined) {
            switch (key) {
              case ('words'):
                q.words = qParams.get(key);
                q.sort = this.sortMethods.RELEVANCE.sortQuery;
                break;
              case ('category'):
                q.category = {id: parseInt(qParams.get(key), 10)};
                break;
              case('ages'):
                q.ages = qParams.getAll(key);
                break;
              case('languages'):
                q.languages = qParams.getAll(key);
                break;
              case('sort'):
                const sortKey = qParams.get(key).toUpperCase();
                if (this.sortMethods[sortKey]) {
                  q.sort = this.sortMethods[sortKey].sortQuery;
                }
                break;
              case('pageStart'):
                q.start = parseInt(qParams.get(key), 10);
                break;
              case('types'):
                q.types = qParams.getAll(key);
                break;
              case('geo_box'):
                const coords = qParams.get(key).split('|').map(s => parseFloat(s));
                q.geo_box = {
                  top_left: {lat: coords[0], lon: coords[1]},
                  bottom_right: {lat: coords[2], lon: coords[3]}
                };
            }
          }
        }
      }
    }

    return q;
  }

  private _updateDistanceSort() {
    this.loadMapLocation(() => {
      this._setDistanceSortLatLong();
      if (this.isDistanceSort) {
        this.selectedSort = this.sortMethods.DISTANCE;
        this.query.sort = this.selectedSort.sortQuery;
        this.query.geo_box = { top_left: {lat: this.mapBounds.getNorthEast().lat(), lon: this.mapBounds.getSouthWest().lng()},
                               bottom_right: {lat: this.mapBounds.getSouthWest().lat(), lon: this.mapBounds.getNorthEast().lng()}};
        console.log(this.query.geo_box);
        this.updateUrlAndDoSearch();
      }
    });
  }

  private _goToFirstPage(skipUpdate = false) {
    this.query.start = 0;
    if (this.paginatorElement) {
      this.paginatorElement.firstPage();
    }

    if (!skipUpdate) {
      this.updateUrlAndDoSearch();
    }
  }

  private _overlaps(a: ClientRect | DOMRect, b: ClientRect | DOMRect): boolean {
    return (
      ((b.top < a.top) && (b.bottom > a.top)) ||      // b overlaps top edge of a
      ((b.top > a.top) && (b.bottom < a.bottom)) ||   // b inside a
      ((b.top < a.bottom) && (b.bottom > a.bottom))   // b overlaps bottom edge of a
    );
  }

  private _queryParamsHaveChanged(qParamMapBefore: ParamMap) {
    const qBefore = this._queryParamsToQuery(qParamMapBefore);
    const qAfter = this._queryParamsToQuery(convertToParamMap(this._queryToQueryParams(this.query)));
    return (!this.prevQuery || qBefore.equals(qAfter));
  }

  private _loadSearchResults() {
    console.log('=== _loadSearchResults ===');
    this.searchService
      .search(this.query)
      .subscribe(queryWithResults => {
        this.query = queryWithResults;
        this.googleAnalyticsService.searchEvent(this.query);
        this.loading = false;
        this.changeDetectorRef.detectChanges();
      });
  }

  private _loadMapResults() {
    this.searchService
      .mapSearch(this.query, !this.restrictToMappedResults)
      .subscribe(mapQueryWithResults => {
        this.mapQuery = mapQueryWithResults;
        if (this.mapQuery && this.mapQuery.hits && (this.mapQuery.hits.length > 0)) {
          this.hitsWithAddress = this.mapQuery.hits.filter(h => !h.no_address);
          this.hitsWithNoAddress = this.mapQuery.hits.filter(h => h.no_address);
        } else {
          this.hitsWithAddress = [];
          this.hitsWithNoAddress = [];
        }

        this.loading = false;
        this.changeDetectorRef.detectChanges();
      });
  }

  private _loadRelatedStudies() {
    const studyQuery = createClone()(this.query);
    studyQuery.types = ['study'];
    this.api.searchStudies(studyQuery).subscribe(results => {
      if (results.hits.length > 0) {
        this.api.getStudy(results.hits[0].id).subscribe(study => {
          this.highlightedStudy = study;
          this.changeDetectorRef.detectChanges();
        });
      } else {
        this.api.getStudiesByStatus('currently_enrolling').subscribe(studies => {
          this.highlightedStudy = studies[Math.floor(Math.random() * Math.floor(studies.length))];
          this.changeDetectorRef.detectChanges();
        });
      }
    });
  }

  private _setDistanceSortLatLong() {
    const distanceSortQuery = this.sortMethods.DISTANCE.sortQuery;
    const useMapLoc = !!(!this.noLocation && this.mapLoc);
    if (this.restrictToMappedResults) {
      distanceSortQuery.latitude = this.mapBounds.getCenter().lat();
      distanceSortQuery.longitude = this.mapBounds.getCenter().lng();
    } else {
      distanceSortQuery.latitude = useMapLoc ? this.mapLoc.lat : this.defaultLoc.lat;
      distanceSortQuery.longitude = useMapLoc ? this.mapLoc.lng : this.defaultLoc.lng;
    }
  }

  private _updatePaginator() {
    const queryStart = this.query && (this.query.start - 1);
    const paramStart = parseInt(this.queryParamMap.get('pageStart'), 10) - 1;
    const pageStart = this.queryParamMap.has('pageStart') ? paramStart : queryStart;
    this.paginatorElement.pageIndex = pageStart / this.pageSize;
    this.expandResults = true;
    this.changeDetectorRef.detectChanges();
  }

  onMapDrag() {
    console.log('map drag');
    this._updateDistanceSort();
  }
}
