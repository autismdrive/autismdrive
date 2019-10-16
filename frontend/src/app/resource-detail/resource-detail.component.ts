import {Component, OnInit} from '@angular/core';
import {ApiService} from '../_services/api/api.service';
import {Resource} from '../_models/resource';
import {User} from '../_models/user';
import {ActivatedRoute} from '@angular/router';
import {LatLngLiteral} from '@agm/core';
import {AuthenticationService} from '../_services/api/authentication-service';
import {AdminNote} from '../_models/admin_note';
import {ContactItem} from '../_models/contact_item';
import {formatDate} from '@angular/common';

@Component({
  selector: 'app-resource-detail',
  templateUrl: './resource-detail.component.html',
  styleUrls: ['./resource-detail.component.scss']
})
export class ResourceDetailComponent implements OnInit {
  resource: Resource;
  mapLoc: LatLngLiteral;
  currentUser: User;
  notes: AdminNote[];
  loading = true;
  contactItems: ContactItem[];
  typeName: string;
  showInfoWindow = false;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private authenticationService: AuthenticationService,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.route.params.subscribe(params => {
      this.loading = true;
      const resourceId = params.resourceId ? parseInt(params.resourceId, 10) : null;

      if (typeof resourceId === 'number' && isFinite(resourceId)) {
        const path = this.route.snapshot.url[0].path;
        const resourceType = path.charAt(0).toUpperCase() + path.slice(1);
        this.api[`get${resourceType}`](resourceId).subscribe(resource => {
          this.resource = new Resource(resource);
          this.initializeContactItems();
          this.loadMapLocation();
          this.loading = false;
        });
        if (this.currentUser && this.currentUser.role === 'Admin') {
          this.api.getResourceAdminNotes(resourceId).subscribe(notes => {
            this.notes = notes;
          })
        }
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
        details: [r.primary_contact]
      },
      {
        condition: !!r.organization,
        icon: 'business',
        details: [r.organization && r.organization.name]
      },
      {
        condition: !!r.date,
        icon: 'access_time',
        details: [r.date && `${formatDate(r.date, 'longDate', 'en-US')}: ${r.time}`]
      },
      {
        condition: !!(r.location_name || r.street_address1 || r.street_address2 || r.city || r.state || r.zip),
        icon: 'location_on',
        details: [r.location_name, r.street_address1, r.street_address2, `${r.city ? r.city + ',' : r.city} ${r.state} ${r.zip}`],
        type: 'address',
      },
      {
        condition: !!r.ticket_cost,
        icon: 'monetization_on',
        details: [r.ticket_cost]
      },
      {
        condition: !!r.phone,
        icon: 'phone',
        details: [r.phone],
        type: 'phone',
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
