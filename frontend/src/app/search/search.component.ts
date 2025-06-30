/// <reference types="@types/google.maps" />
import {animate, query, stagger, style, transition, trigger} from '@angular/animations';
import {CommonModule, Location} from '@angular/common';
import {
  AfterViewInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  effect,
  HostBinding,
  OnInit,
  signal,
  ViewChild,
  WritableSignal,
} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {MatCardModule} from '@angular/material/card';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatPaginator, MatPaginatorModule, PageEvent} from '@angular/material/paginator';
import {MatSelectModule} from '@angular/material/select';
import {MatTabChangeEvent, MatTabsModule} from '@angular/material/tabs';
import {MatTooltipModule} from '@angular/material/tooltip';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, convertToParamMap, ParamMap, Params, Router, RouterModule} from '@angular/router';
import {AddButtonComponent} from '@app/add-button/add-button.component';
import {BorderBoxTileComponent} from '@app/border-box-tile/border-box-tile.component';
import {LoadingComponent} from '@app/loading/loading.component';
import {SearchBoxComponent} from '@app/search-box/search-box.component';
import {SearchFilterComponent} from '@app/search-filter/search-filter.component';
import {SearchFiltersBreadcrumbsComponent} from '@app/search-filters-breadcrumbs/search-filters-breadcrumbs.component';
import {SearchResultComponent} from '@app/search-result/search-result.component';
import {SearchSortComponent} from '@app/search-sort/search-sort.component';
import {SearchTopicsComponent} from '@app/search-topics/search-topics.component';
import {paramMapsAreEqual} from '@app/shared/utilities/map-equals';
import {TutorialVideoComponent} from '@app/tutorial-video/tutorial-video.component';
import {TypeIconComponent} from '@app/type-icon/type-icon.component';
import {Algorithm, DefaultRenderer, Renderer, SuperClusterViewportAlgorithm} from '@googlemaps/markerclusterer';
import {AccordionItem} from '@models/accordion-item';
import {Category} from '@models/category';
import {AgeRange, HitType, Language} from '@models/hit_type';
import {NavItem} from '@models/nav-item';
import {GeoBox, Hit, Query, QueryProps} from '@models/query';
import {Resource} from '@models/resource';
import {Direction} from '@models/scroll';
import {SortMethod, sortMethods} from '@models/sort_method';
import {Study} from '@models/study';
import {User} from '@models/user';
import {NgMapsCoreModule, NgMapsViewComponent} from '@ng-maps/core';
import {NgMapsGoogleModule} from '@ng-maps/google';
import {NgMapsMarkerClustererModule} from '@ng-maps/marker-clusterer';
import {ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';
import {SearchService} from '@services/search/search.service';
import {StorageService} from '@services/storage/storage.service';
import createClone from 'rfdc';
import {firstValueFrom, fromEvent} from 'rxjs';
import {filter, map, pairwise, share, throttleTime} from 'rxjs/operators';

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
  standalone: true,
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
  imports: [
    AddButtonComponent,
    BorderBoxTileComponent,
    CommonModule,
    ExtendedModule,
    FlexModule,
    FormsModule,
    LoadingComponent,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatPaginatorModule,
    MatSelectModule,
    MatTabsModule,
    MatTooltipModule,
    NgMapsCoreModule,
    NgMapsGoogleModule,
    NgMapsMarkerClustererModule,
    ReactiveFormsModule,
    RouterModule,
    SearchBoxComponent,
    SearchFilterComponent,
    SearchFiltersBreadcrumbsComponent,
    SearchResultComponent,
    SearchSortComponent,
    SearchTopicsComponent,
    TutorialVideoComponent,
    TypeIconComponent,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SearchComponent implements AfterViewInit, OnInit {
  @HostBinding('@pageAnimations')
  public animatePage = true;

  query: WritableSignal<Query> = signal<Query>(null);
  mapQuery: WritableSignal<Query> = signal<Query>(null);
  shouldShowMap: WritableSignal<boolean> = signal(false);
  loading: WritableSignal<boolean> = signal(true);
  queryParamMap: WritableSignal<ParamMap> = signal(convertToParamMap({}));

  prevQueryParamMap: ParamMap = convertToParamMap({});
  prevQuery: Query = null;
  prevMapQuery: Query = null;
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
  sortMethods: Record<string, SortMethod>;
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
      image: '/public/partners/craag.png',
      url: 'https://www.cahumanservices.org/craag/',
    },
    {
      name: 'The Faison Center',
      shortName: 'Faison Center',
      description: 'The Faison School provides full-time day school programs for students ages 5 to 22 years.',
      image: '/public/partners/faison_center.png',
      url: 'https://www.faisoncenter.org',
    },
    {
      name: 'Piedmont Regional Education Program',
      shortName: 'PREP',
      description: `
        A public regional organization designed to meet the needs of special education students. Provides special
        education programming and related services to nine school districts under an umbrella of a regional program.
      `,
      image: '/public/partners/prep.png',
      url: 'https://www.prepivycreek.com/',
    },
    {
      name: 'Virginia Institute of Autism',
      shortName: 'VIA',
      description: `
        The Virginia Institute of Autism is dedicated to helping people overcome the challenges of autism through innovative,
        evidence-based programs in education, outreach and adult services.
      `,
      image: '/public/partners/via.png',
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
  mapBounds: google.maps.LatLngBoundsLiteral;
  scrollDirection: Direction;
  clusterAlgorithm: Algorithm = new SuperClusterViewportAlgorithm({maxZoom: 8});
  clusterRenderer: Renderer = new DefaultRenderer();
  readonly panelOpenState = signal(false);
  skipUpdate = false;

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
    private googleMapsLibrary: GoogleMapsLibraryService,
    private storageService: StorageService,
  ) {
    // Watch for changes to the query param map, and update the query signal when it changes.
    effect(() => {
      // Only update the query signal if the URL params have changed.
      const newParamMap = this.queryParamMap();
      if (!this.queryParamsHaveChanged(this.prevQueryParamMap, newParamMap)) return;

      this.prevQueryParamMap = createClone()(newParamMap);

      // Only update the query signal if the query has changed.
      const newQuery = this.queryParamsToQuery(newParamMap);
      if (!this.queryHasChanged(this.prevQuery, newQuery)) return;
      this.prevQuery = createClone()(newQuery);
      this.query.set(newQuery);
    });

    // Watch for changes to the map query signal, and update the URL when it changes.
    effect(() => {
      // Only update the map query if we should be showing the map.
      if (!this.shouldShowMap()) return;

      // Only update the query signal if the URL params have changed.
      const newParamMap = this.queryParamMap();
      if (!this.queryParamsHaveChanged(this.prevQueryParamMap, newParamMap)) return;

      this.prevQueryParamMap = createClone()(newParamMap);

      // Only update the map query signal if the map query has changed.
      const newMapQuery = this.queryParamsToQuery(newParamMap);
      if (!this.queryHasChanged(this.prevMapQuery, newMapQuery)) return;
      this.prevMapQuery = createClone()(newMapQuery);
      this.mapQuery.set(newMapQuery);
    });

    // Watch for changes to the map query, and run a map search when it changes.
    effect(async () => {
      const newMapQuery = this.mapQuery();

      // Only run the search if the new map query is different from the current one.
      if (!this.queryHasChanged(this.prevMapQuery, newMapQuery)) return;

      this.loading.set(true);
      const geoBox = this.geoBox();
      const mapQueryWithResults = await firstValueFrom(this.searchService.mapSearch(newMapQuery, geoBox));
      this.mapQuery.set(mapQueryWithResults);

      if (mapQueryWithResults?.hits?.length > 0) {
        this.hitsWithAddress = mapQueryWithResults.hits.filter(h => !h.no_address);
        this.hitsWithNoAddress = mapQueryWithResults.hits.filter(h => h.no_address);
      } else {
        this.hitsWithAddress = [];
        this.hitsWithNoAddress = [];
      }

      // Update the UI with the new results.
      this.loading.set(false);
      this.changeDetectorRef.detectChanges();

      // If we are restricting to mapped results, update the main query to match the map results.
      if (this.restrictToMappedResults) {
        this.query.update(q => new Query({...q, geo_box: geoBox}));
      }
    });

    // Watch for changes to the current user.
    effect(() => {
      this.currentUser = this.authenticationService.currentUser();
    });

    // Watch for changes to the map library loading status.
    effect(() => {
      this.googleMapsLibrary.core();
      this.updateShouldShowMap();
    });

    // Watch for changes to the query signal.
    effect(async () => {
      const newQuery = this.query();

      // Only run the search if the new query is different from the current one.
      if (!this.queryHasChanged(this.prevQuery, newQuery)) return;

      // Get the results from the API.
      this.loading.set(true);
      const queryWithResults = await firstValueFrom(this.searchService.search(newQuery));
      this.query.set(queryWithResults);

      // Log the search event to Google Analytics.
      this.googleAnalyticsService?.searchEvent(queryWithResults);

      // Update the query parameters in the URL.
      this.updateUrl();

      // Update the UI with the new results.
      this.loading.set(false);
      this.changeDetectorRef.detectChanges();
      await this.loadRelatedStudies();
      this.updatePaginator();
    });

    this.sortMethods = createClone()(sortMethods);
    this.sortMethods['DISTANCE'].sortQuery.latitude = this.loc.lat;
    this.sortMethods['DISTANCE'].sortQuery.longitude = this.loc.lng;
    this.selectedSort = this.sortMethods['DISTANCE'];
    this.languageOptions = Language.options;
    this.ageOptions = AgeRange.options;

    this.meta.updateTag(
      {property: 'og:image', content: window.location.origin + '/public/home/hero-parent-child.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: window.location.origin + '/public/home/hero-parent-child.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: window.location.origin + '/public/home/hero-parent-child.jpg'},
      `name='twitter:image'`,
    );
  }

  get mapsCoreLibrary() {
    const core = this.googleMapsLibrary.core();

    if (!core) {
      console.error('Google Maps Library is not loaded yet.');
    }

    return core;
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
    return this.query()?.hits;
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
    return this.query()?.total || 0;
  }

  get shouldHideVideo() {
    return !!this.storageService.get('shouldHideTutorialVideo');
  }

  updateShouldShowMap() {
    const isLocation = this.selectedType && ['event', 'location'].includes(this.selectedType.name);
    this.shouldShowMap.set(this.mapsCoreLibrary && (isLocation || this.isDistanceSort));
  }

  get selectedCategory() {
    return this.query()?.category;
  }

  get resourceTypesFiltered(): HitType[] {
    return this.resourceTypes.filter(t => t.name !== HitType.ALL_RESOURCES.name);
  }

  ngOnInit() {
    if (this.storageService.get('noFirstVisit') === 'true') {
      this.hideVideo();
    }
    this.storageService.set('noFirstVisit', 'true');

    /**
     * On initialization, set up two subjects that will watch for, debounce, and deduplicate all queries sent to
     * the backend.  Then attempt to run a sensible search, either based on query params or using defaults.
     * In the even we can fall back to the users current location, we may need to run the query again, but
     * we don't want to wait for them to grant us access, so in the worst case, we just run the query using a
     * default location in central Virginia, and if we get GPS, we run it again.
     */

    this.setDefaultMapLocation(async () => {
      const qParamMap = await firstValueFrom(this.route.queryParamMap);
      this.queryParamMap.set(qParamMap);
      this.query.set(this.queryParamsToQuery(qParamMap));

      const defaultZoomLevel = this.storedZip ? 10 : this.defaultZoom;
      this.mapZoomLevel = parseInt(qParamMap.get('zoom')) || defaultZoomLevel;

      // parse lat and lng from URL
      const qLat = qParamMap.get('lat');
      const qLng = qParamMap.get('lng');
      if (qLat && qLng) {
        const lat = parseFloat(qLat);
        const lng = parseFloat(qLng);
        this.setLocation(LocationMode.map, {lat: lat, lng: lng});
      }

      const queryValue = this.query();
      const sortName = qParamMap.get('sort') || (queryValue.hasWords ? 'Relevance' : 'Distance');
      this.reSort(sortName, true);
      this.mapQuery.set(this.query());
    });
  }

  setLocation(mode: LocationMode, loc: google.maps.LatLngLiteral) {
    this.loc = loc;
    this.locationMode = mode;

    this.query.update(
      q =>
        new Query({
          ...q,
          sort: {
            ...q.sort,
            latitude: this.loc.lat,
            longitude: this.loc.lng,
          },
          geo_box: this.geoBox(),
        }),
    );
    this.mapQuery.set(this.query());
  }

  async setZipLocation(zipCode: string, callback?: () => void) {
    this.storedZip = zipCode;
    const z = await firstValueFrom(this.api.getZipCoords(this.storedZip));
    this.setLocation(LocationMode.zipcode, {lat: z.latitude, lng: z.longitude});
    this.mapZoomLevel = 10;
    if (callback) {
      callback();
    }
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

  removeCategory() {
    this.query.update(q => new Query({...q, category: null}));
    this.goToFirstPage();
  }

  removeWords() {
    this.query.update(q => new Query({...q, words: ''}));
    this.goToFirstPage();
  }

  scrollToTopOfSearch() {
    document.getElementById('TopOfSearch').scrollIntoView();
  }

  async setDefaultMapLocation(callback?: () => void) {
    /**
     * If a zipcode is defined, use the zipcode lat and long.
     * If no zipcode, use the browsers gps Location (if we can get it).
     * Otherwise, just leave it as the default.
     *
     * This is just setting up the defaults during initial load, these will likely be overridden
     * as users interact with the map.
     *
     * 1) Sets the mapLoc variable and noLocation variables
     * 2) Calls _setDistanceSortLatLog, which updates the distanceSortQuery to use new mapLoc.
     * 3) Finally, calls the given callback.
     *
     */
    this.storedZip = this.storageService.get('zipCode');
    if (this.isZipCode(this.storedZip)) {
      await this.setZipLocation(this.storedZip, callback);
    } else {
      this.setLocation(LocationMode.default, this.defaultLoc);
      if (callback) {
        callback(); // Don't wait for GPS, we may not get it, just use the default location.
      }
      this.setGPSLocation(() => {
        // Reload if the call is successful AND we have a gps location
        if (this.gpsEnabled) {
          this.reSort('Distance', true);
        }
      });
    }
  }

  reSort(sortName: string, forceReSort = false) {
    const newParamMap = this.queryParamMap();

    // Don't re-sort if the query hasn't changed.
    const qParamsHaveChanged = this.queryParamsHaveChanged(this.prevQueryParamMap, newParamMap);

    // Don't re-sort if it's already selected, but allow override.
    if ((qParamsHaveChanged && sortName && sortName !== this.selectedSort.name) || forceReSort) {
      this.selectedSort = this.sortMethods[sortName.toUpperCase()] || this.sortMethods['DISTANCE'];
      this.query.update(q => new Query({...q, start: 0, sort: this.selectedSort.sortQuery}));

      if (this.isDistanceSort) {
        this.updateDistanceSort();
      }

      // Update the map query to match the main query.
      this.mapQuery.set(this.query());
    }
  }

  selectAgeRange(age: string = '') {
    this.query.update(q => new Query({...q, ages: age?.length > 0 ? [age] : []}));
    this.goToFirstPage();
  }

  selectLanguage(language: string = '') {
    this.query.update(q => new Query({...q, languages: language?.length > 0 ? [language] : []}));
    this.goToFirstPage();
  }

  selectCategory(newCategory: Category) {
    // When selecting a category, clean it down to just what we need to do a search
    this.query.update(q => new Query({...q, category: {id: newCategory.id, name: newCategory.name}}));
    this.goToFirstPage();
  }

  selectType(keepType: string = null) {
    const all = HitType.ALL_RESOURCES.name;
    const forceReSort = !(keepType && keepType !== all);

    this.selectedTypeTabIndex = this.resourceTypes.findIndex(t => (forceReSort ? t.name === keepType : t.name === all));
    this.selectedType = this.resourceTypes[this.selectedTypeTabIndex];
    const sortMethod = this.getSortMethod(forceReSort, keepType);
    this.selectedSort = this.sortMethods[sortMethod];

    this.query.update(
      q =>
        new Query({
          ...q,
          types: forceReSort || keepType === all ? this.resourceTypesFilteredNames() : [keepType],
          date: !forceReSort || keepType === HitType.EVENT.name ? new Date() : undefined,
          sort: this.selectedSort.sortQuery,
        }),
    );

    this.goToFirstPage();
    this.reSort(this.selectedSort.name, forceReSort);
  }

  private getSortMethod(forceReSort: boolean, hitType: string) {
    if (forceReSort) return 'DISTANCE';

    switch (hitType) {
      case HitType.LOCATION.name:
        return 'DISTANCE';
      case HitType.RESOURCE.name:
        return this.query().hasWords ? 'RELEVANCE' : 'UPDATED';
      case HitType.EVENT.name:
        return 'DATE';
      default:
        return 'DISTANCE';
    }
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
    this.query.update(
      q =>
        new Query({
          ...q,
          size: event.pageSize,
          start: event.pageIndex * event.pageSize + 1,
          sort: this.selectedSort.sortQuery,
        }),
    );
    this.pageSize = event.pageSize;
    this.scrollToTopOfSearch();
  }

  showBreadcrumbs(): boolean {
    return !!this.query().hasFilters;
  }

  submitZip($event: Event): void {
    this.panelOpenState.set(false);
    $event.stopPropagation();
    this.storageService.set('zipCode', this.storedZip);
    this.googleAnalyticsService?.searchInteractionEvent('set_zip_code_location');
    if (this.isZipCode(this.storedZip)) {
      this.mapZoomLevel = 10;
      this.setZipLocation(this.storedZip, () => {
        this.reSort('Distance', true);
      });
    } else {
      this.setLocation(LocationMode.default, this.defaultLoc);
    }
  }

  useGPSLocation($event: Event): void {
    this.panelOpenState.set(false);
    $event.stopPropagation();
    this.googleAnalyticsService?.searchInteractionEvent('set_gps_location');
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
      this.googleAnalyticsService?.mapEvent(hit.id.toString());
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
    this.mapQuery.set(this.query());
  }

  selectTypeTab($event: MatTabChangeEvent) {
    const resourceType = $event.index > 0 ? this.resourceTypesFiltered[$event.index - 1] : HitType.ALL_RESOURCES;
    this.selectType(resourceType.name);
  }

  updateResultsList($event: google.maps.LatLngBoundsLiteral) {
    this.mapBounds = $event;
  }

  geoBox(): GeoBox | undefined {
    if (this.mapBounds && this.mapsCoreLibrary) {
      const latLngBounds = new this.mapsCoreLibrary.LatLngBounds(this.mapBounds);
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

    return undefined;
  }

  listMapResultsOnly(shouldRestrict: boolean) {
    this.restrictToMappedResults = shouldRestrict;
    if (shouldRestrict) {
      this.googleAnalyticsService?.searchInteractionEvent('search_as_map_moves');
    }

    this.query.update(q => new Query({...q, geo_box: shouldRestrict ? this.geoBox() : null}));
  }

  mapDockClass(scrollSpy: HTMLSpanElement, searchHeader: HTMLDivElement, searchFooter: HTMLDivElement): string {
    const scrollSpyPos = scrollSpy.getBoundingClientRect();
    const headerPos = searchHeader.getBoundingClientRect();
    const footerPos = searchFooter.getBoundingClientRect();
    const scrollDirection = this.scrollDirection ? this.scrollDirection.toLowerCase() : '';

    let alignClass: string;

    if (this.overlaps(scrollSpyPos, headerPos)) {
      alignClass = 'align-top';
    } else if (this.overlaps(scrollSpyPos, footerPos)) {
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
      map(_ => window.scrollY),
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
    this.skipUpdate = true;
    this.listMapResultsOnly(false);
    this.removeWords();
    this.selectAgeRange(null);
    this.selectLanguage(null);
    this.selectType(null);
    this.removeCategory();
  }

  toggleShowFilters() {
    this.showFilters = !this.showFilters;

    if (!this.shouldShowMap()) {
      this.expandResults = true;
    }
  }

  goSelectedMapResource(selectedMapResource: Resource) {
    this.googleAnalyticsService?.mapResourceEvent(selectedMapResource.id.toString());
    this.router.navigate(['/' + selectedMapResource.type.toLowerCase() + '/' + selectedMapResource.id]);
  }

  hideVideo(shouldHide = true) {
    if (shouldHide) {
      this.storageService.set('shouldHideTutorialVideo', `${shouldHide}`);
    } else {
      this.storageService.remove('shouldHideTutorialVideo');
    }
  }

  showLocationWindow() {
    return this.locationMode === LocationMode.default && !this.isZipCode(this.storedZip) && !this.gpsEnabled;
  }

  updateUrl() {
    const qParams = this.queryToQueryParams(this.query());
    const urlTree = this.router.createUrlTree([], {
      queryParams: qParams,
      queryParamsHandling: 'merge',
      preserveFragment: true,
    });
    this.location.replaceState(urlTree.toString());
  }

  protected mapLoad(m: google.maps.Map) {
    if (!this.mapsCoreLibrary) return;

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
    controlText.innerHTML = '<img src="/public/map/my-location.svg" alt="Your Location">';
    controlUI.appendChild(controlText);

    // Set the center to the user's location on click
    controlUI.addEventListener('click', event => {
      // Get GPS location, and if we have it, set the map to that location.
      this.useGPSLocation(event);
    });

    controlDiv.index = 1;
    m.controls[this.mapsCoreLibrary.ControlPosition.RIGHT_BOTTOM].push(controlDiv);

    m.addListener('dragend', () => {
      const latLngBounds = new this.mapsCoreLibrary.LatLngBounds(this.mapBounds);
      this.setLocation(LocationMode.map, {
        lat: latLngBounds.getCenter().lat(),
        lng: latLngBounds.getCenter().lng(),
      });

      if (this.isDistanceSort) {
        this.updateDistanceSort();
      }
    });
  }

  updateDistanceSort() {
    const distanceSortQuery = this.sortMethods['DISTANCE'].sortQuery;
    distanceSortQuery.latitude = this.loc.lat;
    distanceSortQuery.longitude = this.loc.lng;
    this.query.update(q => new Query({...q, sort: distanceSortQuery}));
  }

  queryToQueryParams(qBefore: Query): Params {
    const q = createClone({circles: true})(qBefore);
    const queryParams: Params = {};

    if (q.hasOwnProperty('words') && q.words) {
      queryParams['words'] = q.words;
    }

    queryParams['types'] = q.types;
    queryParams['ages'] = q.ages;
    queryParams['languages'] = q.languages;
    queryParams['sort'] = queryParams['words'] ? this.sortMethods['RELEVANCE'].name : this.selectedSort.name;
    queryParams['pageStart'] = q.start || 0;
    queryParams['zoom'] = this.mapZoomLevel;
    queryParams['restrictToMap'] = this.restrictToMappedResults ? 'y' : 'n';
    if (this.loc) {
      // Only do this if there is a map location.
      queryParams['lat'] = this.loc.lat; // ? this.mapLoc.lat : this.defaultLoc.lat;
      queryParams['lng'] = this.loc.lng; // ? this.mapLoc.lng : this.defaultLoc.lng;
    }

    if (q.hasOwnProperty('category') && q.category) {
      queryParams['category'] = q.category.id;
    }
    return queryParams;
  }

  queryParamsToQuery(qParams: ParamMap): Query {
    const q: QueryProps = {
      geo_box: undefined,
      words: '',
      ages: [],
      languages: [],
      sort: this.sortMethods['DISTANCE'].sortQuery,
      start: 0,
      types: this.resourceTypesFilteredNames(),
    };
    q.size = this.pageSize;
    if (qParams?.keys) {
      for (const key of qParams.keys) {
        switch (key) {
          case 'words':
            q.words = qParams.get(key);
            q.sort = this.sortMethods['RELEVANCE'].sortQuery;
            break;
          case 'category':
            q.category = {id: parseInt(qParams.get(key))};
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
            q.start = parseInt(qParams.get(key));
            break;
          case 'types':
            q.types = qParams.getAll(key);
            break;
          case 'restrictToMap':
            this.restrictToMappedResults = qParams.get('restrictToMap') === 'y';
            break;
          default:
            break;
        }
      }
    }
    return new Query(q);
  }

  goToFirstPage() {
    this.query.update(q => new Query({...q, start: 0}));
    this.paginatorElement?.firstPage();
  }

  overlaps(a: DOMRect, b: DOMRect): boolean {
    return (
      (b.top < a.top && b.bottom > a.top) || // b overlaps top edge of a
      (b.top > a.top && b.bottom < a.bottom) || // b inside a
      (b.top < a.bottom && b.bottom > a.bottom) // b overlaps bottom edge of a
    );
  }

  queryParamsHaveChanged(prevMap: ParamMap, newMap: ParamMap): boolean {
    return !prevMap || paramMapsAreEqual(prevMap, newMap);
  }

  queryHasChanged(prevQuery: Query, newQuery: Query): boolean {
    return !prevQuery || !prevQuery.equals(newQuery);
  }

  async loadRelatedStudies() {
    const studyQuery = createClone()(this.query());
    studyQuery.types = ['study'];
    const results = await firstValueFrom(this.api.searchStudies(studyQuery));
    if (results.hits.length > 0) {
      this.highlightedStudy = await firstValueFrom(this.api.getStudy(results.hits[0].id));
    } else {
      const studies = await firstValueFrom(this.api.getStudiesByStatus('currently_enrolling'));
      this.highlightedStudy = studies[Math.floor(Math.random() * Math.floor(studies.length))];
    }
    this.changeDetectorRef.detectChanges();
  }

  updatePaginator() {
    const q = this.query();
    const pageStart = q.start ? q.start - 1 : 0;
    this.paginatorElement.pageIndex = pageStart / this.pageSize;
    this.expandResults = true;
    this.changeDetectorRef.detectChanges();
  }

  makePoint(x: number, y: number): google.maps.Point | undefined {
    return !this.mapsCoreLibrary ? undefined : new this.mapsCoreLibrary.Point(x, y);
  }

  updateQueryParams(newParams: Params) {
    this.queryParamMap.set(convertToParamMap(newParams));
    this.query.set(this.queryParamsToQuery(this.queryParamMap()));
    this.updateUrl();
  }
}
