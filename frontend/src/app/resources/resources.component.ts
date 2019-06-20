import { LatLngLiteral } from '@agm/core';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { HitLabel, HitType, Query } from '../_models/query';
import { ApiService } from '../_services/api/api.service';
import { SearchService } from '../_services/api/search.service';

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
    return {name: HitType[t], label: HitLabel[t] };
  });
  query: Query;
  mapLoc: LatLngLiteral;
  loading = true;

  defaultLoc: LatLngLiteral = {
    lat: 37.9864031,
    lng: -81.6645856
  };

  constructor(
    private api: ApiService,
    private searchService: SearchService
  ) {
    this.loadMapLocation(() => this.loadResources());
  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    this.searchService.reset();
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

  loadResources() {
    this.loading = true;

    this.query = new Query({filters: [{field: 'Type', value: HitLabel.LOCATION}]});
    if (this.mapLoc) {
      this.query.sort = {
        field: 'geo_point',
        latitude: this.mapLoc.lat,
        longitude: this.mapLoc.lng,
        order: 'asc',
        unit: 'mi'
      };
    }

    this.searchService
      .search(this.query)
      .subscribe(queryWithResults => {
        if (this.query.equals(queryWithResults)) {
          this.query = queryWithResults;
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
    if (this.query) {
      console.log(this.query.hits);
    }
  }
}

