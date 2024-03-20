/// <reference types="@types/googlemaps" />
import {formatDate} from '@angular/common';
import {Component, OnInit} from '@angular/core';
import {DomSanitizer, SafeResourceUrl} from '@angular/platform-browser';
import {ActivatedRoute, Router} from '@angular/router';
import {ContactItem} from '../_models/contact_item';
import {Resource} from '../_models/resource';
import {ResourceChangeLog} from '../_models/resource_change_log';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import LatLngLiteral = google.maps.LatLngLiteral;

@Component({
  selector: 'app-resource-detail',
  templateUrl: './resource-detail.component.html',
  styleUrls: ['./resource-detail.component.scss'],
})
export class ResourceDetailComponent implements OnInit {
  resource: Resource;
  mapLoc: LatLngLiteral;
  currentUser: User;
  changeLog: ResourceChangeLog[];
  loading = true;
  contactItems: ContactItem[];
  typeName: string;
  showInfoWindow = false;
  safeVideoLink: SafeResourceUrl;
  get isPastEvent(): boolean {
    const eventDate = new Date(this.resource.date);
    const now = new Date();

    console.log('eventDate', eventDate);
    return !!(
      this.resource &&
      this.resource.type === 'event' &&
      eventDate < now &&
      this.resource.post_event_description
    );
  }

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
    private _sanitizer: DomSanitizer,
  ) {
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
    this.route.params.subscribe(params => {
      this.loading = true;
      this.safeVideoLink = null;
      const resourceId = params.resourceId ? parseInt(params.resourceId, 10) : null;

      if (typeof resourceId === 'number' && isFinite(resourceId)) {
        const path = this.route.snapshot.url[0].path;
        const resourceType = path.charAt(0).toUpperCase() + path.slice(1);
        this.api[`get${resourceType}`](resourceId).subscribe(resource => {
          this.resource = new Resource(resource);

          console.log('resource = ', this.resource);

          this.initializeContactItems();
          this.loadMapLocation();
          this.loading = false;
          if (this.resource.video_code) {
            this.safeVideoLink = this._sanitizer.bypassSecurityTrustResourceUrl(
              'https://www.youtube.com/embed/' + this.resource.video_code,
            );
          }
          if (this.currentUser && this.currentUser.permissions.includes('edit_resource')) {
            this.api.getResourceChangeLog(this.resource.id).subscribe(log => {
              this.changeLog = log;
            });
          }
        });
      }
    });
  }

  get userCanEdit(): boolean {
    return this.currentUser && this.currentUser.permissions.includes('edit_resource');
  }

  get resourceIsDraft(): boolean {
    return this.resource.is_draft === true;
  }

  ngOnInit() {}

  loadMapLocation() {
    if (this.resource && this.resource.hasCoords() && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(p => {
        this.mapLoc = {
          lat: p.coords.latitude,
          lng: p.coords.longitude,
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
      window.open(this.resource.website, '_blank');
    }
  }

  getGoogleMapsUrl(): string {
    if (this.mapLoc && this.resource.hasCoords()) {
      const address = `
        ${this.resource.street_address1},
        ${this.resource.street_address2},
        ${this.resource.city},
        ${this.resource.state}
        ${this.resource.zip}
      `;

      return `https://www.google.com/maps/dir/${this.mapLoc.lat},${this.mapLoc.lng}/${encodeURIComponent(address)}`;
    }
  }

  initializeContactItems() {
    const r = this.resource;
    this.contactItems = [
      {
        condition: !!r.primary_contact,
        icon: 'person_pin',
        details: [r.primary_contact],
      },
      {
        condition: !!r.organization_name,
        icon: 'business',
        details: [r.organization_name],
      },
      {
        condition: !!r.date,
        icon: 'access_time',
        details: [r.date && `${formatDate(r.date, 'longDate', 'en-US', '-0')}: ${r.time}`],
      },
      {
        condition: !!(r.location_name || r.street_address1 || r.street_address2 || r.city || r.state || r.zip),
        icon: 'location_on',
        details: [
          r.location_name,
          r.street_address1,
          r.street_address2,
          `${r.city ? r.city + ',' : r.city} ${r.state} ${r.zip}`,
        ],
        type: 'address',
      },
      {
        condition: !!r.ticket_cost,
        icon: 'monetization_on',
        details: [r.ticket_cost],
      },
      {
        condition: !!r.phone,
        icon: 'phone',
        details: [r.phone],
        type: 'phone',
      },
      {
        condition: !!r.phone_extension,
        icon: 'dialpad',
        details: [r.phone_extension],
        type: 'phone_extension',
      },
      {
        condition: !!r.website,
        icon: 'link',
        details: [r.website],
        type: 'link',
      },
    ];
  }

  toggleInfoWindow($event) {
    this.showInfoWindow = !this.showInfoWindow;
  }
}
