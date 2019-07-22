import { LatLngLiteral } from '@agm/core';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { HitLabel, HitType, Query, Hit } from '../_models/query';
import { SearchService } from '../_services/api/search.service';
import { AccordionItem } from '../_models/accordion-item';
import { AuthenticationService } from '../_services/api/authentication-service';
import { User } from '../_models/user';

interface MostRecents {
  resource: Hit;
  location: Hit;
  event: Hit;
}

interface ResourceType {
  name: string;
  label: string;
}

class MapControlDiv extends HTMLDivElement {
  index?: number;
}

@Component({
  selector: 'app-resources',
  templateUrl: './resources.component.html',
  styleUrls: ['./resources.component.scss']
})
export class ResourcesComponent implements OnInit, OnDestroy {
  resourceTypes: ResourceType[] = ['RESOURCE', 'LOCATION', 'EVENT'].map(t => {
    return { name: HitType[t], label: HitLabel[t] };
  });

  resourceGatherers: AccordionItem[] = [
    {
      name: 'Charlottesville Region Autism Action Group',
      shortName: 'CRAAG',
      description: `
        CRAAG is a parent-run advocacy group, one of three active all-volunteer regional Autism Action Groups
        initiated by Commonwealth Autism. Established in 2010, it serves Charlottesville, Albemarle, Greene,
        Fluvanna, Louisa, and Nelson counties.
      `,
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
      url: 'https://curry.virginia.edu/faculty-research/centers-labs-projects/supporting-transformative-autism-research-star',
    }
  ];
  locQuery: Query;
  recentQuery: Query;
  mapLoc: LatLngLiteral;
  loading = true;

  defaultLoc: LatLngLiteral = {
    lat: 37.9864031,
    lng: -81.6645856
  };

  mostRecents: MostRecents = {
    resource: null,
    location: null,
    event: null,
  };

  currentUser: User;

  constructor(
    private locSearchService: SearchService,
    private recentSearchService: SearchService,
    private authenticationService: AuthenticationService,
  ) {
    this.loadMapLocation(() => this.loadLocResources());
    this.loadRecentResources();
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);

  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    this.locSearchService.reset();
    this.recentSearchService.reset();
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

  loadRecentResources() {
    this.loading = true;

    this.resourceTypes.forEach(resourceType => {
      this.recentQuery = new Query({
        sort: { field: 'last_updated', order: 'desc' },
        filters: [{ field: 'Type', value: resourceType.label }],
        size: 1,
        start: 0,
      });

      this.recentSearchService
        .search(this.recentQuery)
        .subscribe(queryWithResults => {
          if (this.recentQuery.equals(queryWithResults)) {
            const result = (queryWithResults.hits.length > 0) ? queryWithResults.hits[0] : null;
            this.mostRecents[resourceType.name.toLowerCase()] = result;
            this.loading = !this.mostRecentsLoaded();
          }
        });
    });
  }

  mostRecentsList(): Hit[] {
    return Object.values(this.mostRecents);
  }

  mostRecentsLoaded() {
    return this.mostRecentsList().length === this.resourceTypes.length;
  }

  loadLocResources() {
    this.loading = true;

    this.locQuery = new Query({
      filters: [{ field: 'Type', value: HitLabel.LOCATION }],
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

  protected mapLoad(map: google.maps.Map) {
    this.addMyLocationControl(map);
    this.addMapResources(map);
  }

  addMyLocationControl(map: google.maps.Map) {
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
        map.setCenter(this.mapLoc);
        map.setZoom(9);
      });
    });

    controlDiv.index = 1;
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  }

  addMapResources(map: google.maps.Map) {
    if (this.locQuery) {
      console.log(this.locQuery.hits);
    }
  }
}

