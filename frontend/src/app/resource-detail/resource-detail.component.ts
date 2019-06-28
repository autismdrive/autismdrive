import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Resource } from '../_models/resource';
import { ActivatedRoute } from '@angular/router';
import { LatLngLiteral } from '@agm/core';

@Component({
  selector: 'app-resource-detail',
  templateUrl: './resource-detail.component.html',
  styleUrls: ['./resource-detail.component.scss']
})
export class ResourceDetailComponent implements OnInit {
  resource: Resource;
  mapLoc: LatLngLiteral;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute
  ) {
    this.route.params.subscribe(params => {
      const resourceId = params.resourceId ? parseInt(params.resourceId, 10) : null;

      if (typeof resourceId === 'number' && isFinite(resourceId)) {
        const path = this.route.snapshot.url[0].path;
        const resourceType = path.charAt(0).toUpperCase() + path.slice(1);
        this.api[`get${resourceType}`](resourceId).subscribe(resource => {
          this.resource = new Resource(resource);
          this.loadMapLocation();
        });
      }
    });
  }

  ngOnInit() {
  }

  loadMapLocation() {
    if (this.resource && this.resource.hasCoords() && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        this.mapLoc = {
          lat: p.coords.latitude,
          lng: p.coords.longitude
        };
      });
    }
  }

  goPhone($event: MouseEvent) {
    $event.preventDefault();
    if (this.resource && this.resource.phone) {
      location.href = `tel://${this.resource.phone}`;
    }
  }

  goWebsite($event: MouseEvent) {
    $event.preventDefault();
    if (this.resource && this.resource.website) {
      location.href = this.resource.website;
    }
  }

}
