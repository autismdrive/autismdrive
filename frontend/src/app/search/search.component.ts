/// <reference types="google.maps" />
import {animate, query, stagger, style, transition, trigger} from '@angular/animations';
import {Location} from '@angular/common';
import {AfterViewInit, ChangeDetectorRef, Component, HostBinding, OnInit, ViewChild} from '@angular/core';
import {MatExpansionPanel} from '@angular/material/expansion';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {MatTabChangeEvent} from '@angular/material/tabs';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, convertToParamMap, ParamMap, Params, Router} from '@angular/router';
import {Algorithm, DefaultRenderer, Renderer, SuperClusterViewportAlgorithm} from '@googlemaps/markerclusterer';
import {AccordionItem} from '@models/accordion-item';
import {Category} from '@models/category';
import {AgeRange, HitType, Language} from '@models/hit_type';
import {NavItem} from '@models/nav-item';
import {GeoBox, Hit, Query} from '@models/query';
import {Resource} from '@models/resource';
import {Direction} from '@models/scroll';
import {SortMethod, sortMethods} from '@models/sort_method';
import {Study} from '@models/study';
import {User} from '@models/user';
import {NgMapsViewComponent} from '@ng-maps/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {SearchService} from '@services/search/search.service';
import createClone from 'rfdc';
import {fromEvent, Subject} from 'rxjs';
import {debounceTime, filter, map, pairwise, share, throttleTime} from 'rxjs/operators';

class MapControlDiv extends HTMLDivElement {
  index?: number;
}

enum LocationMode {
  default = 'default',
  zipcode = 'zipcode',
  gps = 'gps',
  map = 'map',
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
          stagger(-30, [animate('500ms cubic-bezier(0.35, 0, 0.25, 1)', style({opacity: 1, transform: 'none'}))]),
        ]),
      ]),
    ]),
  ],
})
export class SearchComponent implements AfterViewInit, OnInit {
  @HostBinding('@pageAnimations')
  public animatePage = true;

  query: Query;
  prevQuery: Query; // Used to tell if query parameters have changed, very unclear.  Consider removing.
  mapQuery: Query; // The Map query is slightly different from the results query, and it returns a larger set of results.
  querySubject: Subject<Query> = new Subject<Query>(); // Use this to update the query.
  mapQuerySubject: Subject<Query> = new Subject<Query>(); // Use this to update the mapQuery.

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

  storedZip: string;
  gpsEnabled = true;
  defaultLoc: google.maps.LatLngLiteral = {
    lat: 37.32248,
    lng: -78.36926,
  };
  loc: google.maps.LatLngLiteral = createClone()(this.defaultLoc);
  locationModes = LocationMode;
  locationMode = LocationMode.default;

  hitsWithNoAddress: Hit[] = [];
  hitsWithAddress: Hit[] = [];
  defaultZoom = 7;
  mapZoomLevel: number;
  sortMethods: {[key: string]: SortMethod};
  selectedSort: SortMethod;
  paginatorElement: MatPaginator;
  mapTemplateElement: NgMapsViewComponent<any>;
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
      url: 'https://www.cahumanservices.org/craag/',
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
      url: 'https://www.prepivycreek.com/',
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
  ];
  queryParamMap: ParamMap;
  private mapBounds: google.maps.LatLngBoundsLiteral;
  private scrollDirection: Direction;
  clusterAlgorithm: Algorithm = new SuperClusterViewportAlgorithm({maxZoom: 8});
  clusterRenderer: Renderer = new DefaultRenderer();

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private changeDetectorRef: ChangeDetectorRef,
    private googleAnalyticsService: GoogleAnalyticsService,
    private location: Location,
    private meta: Meta,
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService,
  ) {
    this.sortMethods = createClone()(sortMethods);
    this.sortMethods.DISTANCE.sortQuery.latitude = this.loc.lat;
    this.sortMethods.DISTANCE.sortQuery.longitude = this.loc.lng;
    this.selectedSort = this.sortMethods.DISTANCE;
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
    this.languageOptions = this.getOptions(Language.labels);
    this.ageOptions = this.getOptions(AgeRange.labels);

    this.meta.updateTag(
      {property: 'og:image', content: window.location.origin + '/assets/home/hero-parent-child.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: window.location.origin + '/assets/home/hero-parent-child.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: window.location.origin + '/assets/home/hero-parent-child.jpg'},
      `name='twitter:image'`,
    );
  }

  @ViewChild('paginator')
  set paginator(value: MatPaginator) {
    this.paginatorElement = value;
  }

  @ViewChild('mapTemplate')
  set mapTemplate(value: NgMapsViewComponent<google.maps.Map>) {
    this.mapTemplateElement = value;
  }

  get circleRadius(): number {
    const maxMiles = 100;
    const metersPerMi = 1609.34;
    return (maxMiles * metersPerMi) / (this.mapZoomLevel || 1);
  }

  get filtersPanelStyles() {
    const styles = {
      'full-screen': this.showFilters,
      minimized: !this.showFilters,
    };

    styles[this.searchBgClass] = true;
    return styles;
  }

  get hits(): Hit[] {
    return this.query.hits;
  }

  get isDistanceSort(): boolean {
    return this.selectedSort && this.selectedSort.name === 'Distance';
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
      return this.paginatorElement.pageIndex * this.pageSize + 1;
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

  get shouldShowMap() {
    const isLocation = this.selectedType && ['event', 'location'].includes(this.selectedType.name);
    return isLocation || this.isDistanceSort;
  }

  get selectedCategory() {
    if (this.query) {
      return this.query.category;
    }
  }

  get resourceTypesFiltered(): HitType[] {
    return this.resourceTypes.filter(t => t.name !== HitType.ALL_RESOURCES.name);
  }

  ngOnInit() {
    if (localStorage.noFirstVisit === 'true') {
      this.hideVideo();
    }
    localStorage.noFirstVisit = true;

    /**
     * On initialization, set up two subjects that will watch for, debouce, and depulicate all queries sent to
     * the backend.  Then attempt to run a sensible search, either based on query params or using defaults.
     * In the even we can fall back to the users current location, we may need to run the query again, but
     * we don't want to wait for them to grant us access, so in the worst case, we just run the query using a
     * default location in central Virginia, and if we get GPS, we run it again.
     */

    this.querySubject.pipe(debounceTime(1000)).subscribe(q => {
      this.loading = true;
      this.searchService.search(q).subscribe(queryWithResults => {
        this.prevQuery = createClone()(this.query);
        this.query = queryWithResults;
        this.googleAnalyticsService.searchEvent(this.query);
        this.updateUrl();
        this.loading = false;
        this.changeDetectorRef.detectChanges();
        this._loadRelatedStudies();
        this._updatePaginator();
      });
    });

    this.setDefaultMapLocation(() => {
      this.route.queryParamMap.subscribe(qParamMap => {
        this.queryParamMap = qParamMap;
        this.query = this._queryParamsToQuery(qParamMap);
        const defaultZoomLevel = this.storedZip ? 10 : this.defaultZoom;
        this.mapZoomLevel = parseInt(qParamMap.get('zoom'), 10) || defaultZoomLevel;
        // parse lat and lng from URL
        const qLat = qParamMap.get('lat');
        const qLng = qParamMap.get('lng');
        if (qLat && qLng) {
          const lat = parseFloat(qLat);
          const lng = parseFloat(qLng);
          this.setLocation(LocationMode.map, {lat: lat, lng: lng});
        }
        const sortName = qParamMap.get('sort') || 'Distance';
        const forceReSort = this.prevQuery && this.query.start === 0;
        if (forceReSort) {
          if (sortName && this.sortMethods[sortName.toUpperCase()]) {
            this.reSort(sortName, forceReSort);
          } else {
            this.reSort(this.query.hasWords ? 'Relevance' : 'Distance', forceReSort);
          }
        } else {
          this.reSort(sortName, true);
          this.selectedSort = this.sortMethods[sortName.toUpperCase()];
          this.querySubject.next(this.query);
          this.mapQuerySubject.next(this.query);
        }
      });
    });
    this.mapQuerySubject.pipe(debounceTime(1000)).subscribe(q => {
      this.loading = true;
      const geoBox = this.geoBox();
      this.searchService.mapSearch(q, geoBox).subscribe(mapQueryWithResults => {
        this.mapQuery = mapQueryWithResults;
        if (this.mapQuery && this.mapQuery.hits && this.mapQuery.hits.length > 0) {
          this.hitsWithAddress = this.mapQuery.hits.filter(h => !h.no_address);
          this.hitsWithNoAddress = this.mapQuery.hits.filter(h => h.no_address);
        } else {
          this.hitsWithAddress = [];
          this.hitsWithNoAddress = [];
        }
        this.loading = false;
        this.changeDetectorRef.detectChanges();
        if (this.restrictToMappedResults) {
          this.query.geo_box = geoBox;
          this.querySubject.next(this.query);
        }
      });
    });
  }

  setLocation(mode: LocationMode, loc: google.maps.LatLngLiteral) {
    this.loc = loc;
    this.locationMode = mode;
  }

  setZipLocation(zipCode: string, callback?: () => void) {
    this.storedZip = zipCode;
    this.api.getZipCoords(this.storedZip).subscribe(z => {
      this.setLocation(LocationMode.zipcode, {lat: z.latitude, lng: z.longitude});
      this.mapZoomLevel = 10;
      if (callback) {
        callback();
      }
    });
  }

  setGPSLocation(callback?: () => void) {
    if (navigator.geolocation) {
      this.gpsEnabled = true;
      navigator.geolocation.getCurrentPosition(
        p => {
          this.setLocation(LocationMode.gps, {lat: p.coords.latitude, lng: p.coords.longitude});
          this.mapZoomLevel = 10;
          if (callback) {
            callback();
          }
        },
        error => {
          console.error(error);
          this.gpsEnabled = false;
          if (callback) {
            callback();
          }
        },
      );
    } else {
      this.gpsEnabled = false;
      if (callback) {
        callback();
      }
    }
  }

  ngAfterViewInit() {
    this.watchScrollEvents();
  }

  getOptions(modelLabels: {[key: string]: string}) {
    const opts = [];
    for (const key in modelLabels) {
      if (modelLabels.hasOwnProperty(key)) {
        opts.push({value: key, label: modelLabels[key]});
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

  setDefaultMapLocation(callback?: () => void) {
    /**
     * If a zipcode is defined, uses the zipcode lat and long.
     * Otherwise use the browsers gps Location if we can get it.
     * Otherwise we just leave it as a default.
     *
     * This is just setting up the defaults during initial load, these will likely be overridden
     * as users interact with the map.
     *
     * 1) Sets the mapLoc variable and noLocation variables
     * 2) Calls _setDistanceSortLatLog, which updates the distanceSortQuery to use new mapLoc.
     * 3) Finally, calls the given callback.
     *
     */
    this.storedZip = localStorage.getItem('zipCode');
    if (this.isZipCode(this.storedZip)) {
      this.setZipLocation(this.storedZip, callback);
    } else {
      this.setLocation(LocationMode.default, this.defaultLoc);
      if (callback) {
        callback(); // Don't wait for GPS, we may not get it, just use the default location.
      }
      this.setGPSLocation(() => {
        // If the call is successful, an we have a gps location, reload.
        if (this.gpsEnabled) {
          this.reSort('Distance', true);
        }
      });
    }
  }

  reSort(sortName: string, forceReSort = false) {
    // Don't re-sort if the query hasn't changed.
    const qParamsHaveChanged = this._queryParamsHaveChanged(this.queryParamMap);

    // Don't re-sort if it's already selected, but allow override.
    if ((qParamsHaveChanged && sortName && sortName !== this.selectedSort.name) || forceReSort) {
      this.selectedSort = this.sortMethods[sortName.toUpperCase()];
      this.query.start = 0;
      this.query.sort = this.selectedSort.sortQuery;

      if (this.isDistanceSort) {
        this._updateDistanceSort();
      }
      this.mapQuerySubject.next(this.query);
      this.querySubject.next(this.query);
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
    // When selecting a category, clean it down to just what we need to do a search
    this.query.category = {id: newCategory.id, name: newCategory.name};
    this._goToFirstPage();
  }

  selectType(keepType: string = null, skipUpdate = false) {
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
      this.query.types = keepType === all ? this.resourceTypesFilteredNames() : [keepType];
      this.query.date = keepType === HitType.EVENT.name ? new Date() : undefined;

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
    const popUp = window.open('https://virginia.az1.qualtrics.com/jfe/form/SV_0JQAQjutv54EwnP', '_blank');
    if (popUp == null || typeof popUp === 'undefined') {
      alert(
        'Please disable your pop-up blocker and try again. \nYou can also use following link to submit your resource: ' +
          'https://virginia.az1.qualtrics.com/jfe/form/SV_0JQAQjutv54EwnP',
      );
    }
  }

  resourceTypesFilteredNames(): string[] {
    return this.resourceTypesFiltered.map(t => t.name);
  }

  updatePage(event: PageEvent) {
    this.query.size = event.pageSize;
    this.pageSize = event.pageSize;
    this.query.start = event.pageIndex * event.pageSize + 1;
    this.query.sort = this.selectedSort.sortQuery;
    this.scrollToTopOfSearch();
    this.querySubject.next(this.query);
  }

  showBreadcrumbs(): boolean {
    return !!(this.query && this.query.hasFilters);
  }

  submitZip($event: MouseEvent | KeyboardEvent, setLocationExpansionPanel: MatExpansionPanel): void {
    setLocationExpansionPanel.close();
    $event.stopPropagation();
    localStorage.setItem('zipCode', this.storedZip);
    this.googleAnalyticsService.searchInteractionEvent('set_zip_code_location');
    if (this.isZipCode(this.storedZip)) {
      this.mapZoomLevel = 10;
      this.setZipLocation(this.storedZip, () => {
        this.reSort('Distance', true);
      });
    } else {
      this.setLocation(LocationMode.default, this.defaultLoc);
    }
  }

  useGPSLocation($event: MouseEvent | KeyboardEvent, setLocationExpansionPanel: MatExpansionPanel): void {
    setLocationExpansionPanel.close();
    $event.stopPropagation();
    this.googleAnalyticsService.searchInteractionEvent('set_gps_location');
    this.setGPSLocation(() => {
      if (this.gpsEnabled) {
        this.reSort('Distance', true);
      }
    });
  }

  isZipCode(zipCode: string): boolean {
    return zipCode && zipCode !== '' && /^\d{5}$/.test(zipCode);
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
    return ((x - Math.floor(x)) / 100) * m;
  }

  updateZoom(zoomLevel: number) {
    this.mapZoomLevel = zoomLevel;
    this.mapQuerySubject.next(this.query);
  }

  selectTypeTab($event: MatTabChangeEvent) {
    const resourceType = $event.index > 0 ? this.resourceTypesFiltered[$event.index - 1] : HitType.ALL_RESOURCES;
    this.selectType(resourceType.name);
  }

  updateResultsList($event: google.maps.LatLngBoundsLiteral) {
    this.mapBounds = $event;
  }

  geoBox(): GeoBox {
    if (this.mapBounds) {
      const latLngBounds = new google.maps.LatLngBounds(this.mapBounds);
      return {
        top_left: {
          lat: latLngBounds.getNorthEast().lat(),
          lon: latLngBounds.getSouthWest().lng(),
        },
        bottom_right: {
          lat: latLngBounds.getSouthWest().lat(),
          lon: latLngBounds.getNorthEast().lng(),
        },
      };
    }
  }

  listMapResultsOnly(shouldRestrict: boolean, skipUpdate = false) {
    console.log('Restricting to mapped results', shouldRestrict);
    this.restrictToMappedResults = shouldRestrict;
    if (shouldRestrict) {
      this.googleAnalyticsService.searchInteractionEvent('search_as_map_moves');
      this.query.geo_box = this.geoBox();
    } else {
      this.query.geo_box = null;
    }

    if (!skipUpdate) {
      this.querySubject.next(this.query);
    }
  }

  mapDockClass(scrollSpy: HTMLSpanElement, searchHeader: HTMLDivElement, searchFooter: HTMLDivElement): string {
    const scrollSpyPos = scrollSpy.getBoundingClientRect();
    const headerPos = searchHeader.getBoundingClientRect();
    const footerPos = searchFooter.getBoundingClientRect();
    const scrollDirection = this.scrollDirection ? this.scrollDirection.toLowerCase() : '';

    let alignClass;

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
      map(e => window.scrollY),
      pairwise(),
      map(([y1, y2]): Direction => (y2 < y1 ? Direction.Up : Direction.Down)),
      share(),
    );

    scroll$.pipe(filter(direction => direction === Direction.Up)).subscribe(() => {
      this.scrollDirection = Direction.Up;
    });

    scroll$.pipe(filter(direction => direction === Direction.Down)).subscribe(() => {
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
    this.querySubject.next(this.query);
    this.mapQuerySubject.next(this.query);
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

  showLocationWindow() {
    return this.locationMode === LocationMode.default && !this.isZipCode(this.storedZip) && !this.gpsEnabled;
  }

  updateUrl() {
    const qParams = this._queryToQueryParams(this.query);
    const urlTree = this.router.createUrlTree([], {
      queryParams: qParams,
      queryParamsHandling: 'merge',
      preserveFragment: true,
    });
    this.location.replaceState(urlTree.toString());
  }

  protected mapLoad(m: google.maps.Map) {
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
    controlText.innerHTML = '<img src="/assets/map/my-location.svg" alt="Your Location">';
    controlUI.appendChild(controlText);

    // Set the center to the user's location on click
    controlUI.addEventListener('click', () => {
      // fixme: maybe we should requery when clicking.
      console.log('map clicked.');
      this.mapQuerySubject.next(this.query);
    });

    controlDiv.index = 1;
    m.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);

    m.addListener('dragend', () => {
      const latLngBounds = new google.maps.LatLngBounds(this.mapBounds);
      this.setLocation(LocationMode.map, {
        lat: latLngBounds.getCenter().lat(),
        lng: latLngBounds.getCenter().lng(),
      });
      this.mapQuerySubject.next(this.query);
      console.log('Map Dragged');
      if (this.isDistanceSort) {
        console.log('Map Dragged, re-sorting');
        this._updateDistanceSort();
        this.querySubject.next(this.query);
      }
    });
  }

  private _updateDistanceSort() {
    const distanceSortQuery = this.sortMethods.DISTANCE.sortQuery;
    distanceSortQuery.latitude = this.loc.lat;
    distanceSortQuery.longitude = this.loc.lng;
    this.query.sort = distanceSortQuery;
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
    queryParams.restrictToMap = this.restrictToMappedResults ? 'y' : 'n';
    if (this.loc) {
      // Only do this if there is a map location.
      queryParams.lat = this.loc.lat; // ? this.mapLoc.lat : this.defaultLoc.lat;
      queryParams.lng = this.loc.lng; // ? this.mapLoc.lng : this.defaultLoc.lng;
    }

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
      types: this.resourceTypesFilteredNames(),
    });
    q.size = this.pageSize;
    if (qParams) {
      if (qParams.keys) {
        for (const key of qParams.keys) {
          if (qParams.get(key) !== undefined) {
            switch (key) {
              case 'words':
                q.words = qParams.get(key);
                q.sort = this.sortMethods.RELEVANCE.sortQuery;
                break;
              case 'category':
                q.category = {id: parseInt(qParams.get(key), 10)};
                break;
              case 'ages':
                q.ages = qParams.getAll(key);
                break;
              case 'languages':
                q.languages = qParams.getAll(key);
                break;
              case 'sort':
                const sortKey = qParams.get(key).toUpperCase();
                if (this.sortMethods[sortKey]) {
                  q.sort = this.sortMethods[sortKey].sortQuery;
                }
                break;
              case 'pageStart':
                q.start = parseInt(qParams.get(key), 10);
                break;
              case 'types':
                q.types = qParams.getAll(key);
                break;
              case 'restrictToMap':
                this.restrictToMappedResults = qParams.get('restrictToMap') === 'y';
                break;
            }
          }
        }
      }
    }
    return q;
  }

  private _goToFirstPage(skipUpdate = false) {
    this.query.start = 0;
    if (this.paginatorElement) {
      this.paginatorElement.firstPage();
    }

    if (!skipUpdate) {
      this.querySubject.next(this.query);
      this.mapQuerySubject.next(this.query);
    }
  }

  private _overlaps(a: ClientRect | DOMRect, b: ClientRect | DOMRect): boolean {
    return (
      (b.top < a.top && b.bottom > a.top) || // b overlaps top edge of a
      (b.top > a.top && b.bottom < a.bottom) || // b inside a
      (b.top < a.bottom && b.bottom > a.bottom) // b overlaps bottom edge of a
    );
  }

  private _queryParamsHaveChanged(qParamMapBefore: ParamMap) {
    const qBefore = this._queryParamsToQuery(qParamMapBefore);
    const qAfter = this._queryParamsToQuery(convertToParamMap(this._queryToQueryParams(this.query)));
    return !this.prevQuery || qBefore.equals(qAfter);
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

  private _updatePaginator() {
    const queryStart = this.query && this.query.start - 1;
    const paramStart = parseInt(this.queryParamMap.get('pageStart'), 10) - 1;
    const pageStart = this.queryParamMap.has('pageStart') ? paramStart : queryStart;
    this.paginatorElement.pageIndex = pageStart / this.pageSize;
    this.expandResults = true;
    this.changeDetectorRef.detectChanges();
  }
}
