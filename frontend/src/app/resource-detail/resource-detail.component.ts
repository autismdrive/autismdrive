/// <reference types="google.maps" />
import {DatePipe, formatDate, NgIf, NgOptimizedImage} from '@angular/common';
import {afterNextRender, ChangeDetectionStrategy, Component, effect} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {DomSanitizer, SafeResourceUrl} from '@angular/platform-browser';
import {ActivatedRoute, Router, RouterModule} from '@angular/router';
import {EditButtonComponent} from '@app/edit-button/edit-button.component';
import {EventRegistrationComponent} from '@app/event-registration/event-registration.component';
import {FavoriteResourceButtonComponent} from '@app/favorite-resource-button/favorite-resource-button.component';
import {TypeIconComponent} from '@app/type-icon/type-icon.component';
import {ContactItem} from '@models/contact_item';
import {Resource} from '@models/resource';
import {ResourceChangeLog} from '@models/resource_change_log';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MarkdownComponent} from 'ngx-markdown';

@Component({
  standalone: true,
  selector: 'app-resource-detail',
  templateUrl: './resource-detail.component.html',
  styleUrls: ['./resource-detail.component.scss'],
  imports: [
    NgOptimizedImage,
    MarkdownComponent,
    FlexModule,
    TypeIconComponent,
    EditButtonComponent,
    FavoriteResourceButtonComponent,
    NgIf,
    EventRegistrationComponent,
    MatButtonModule,
    DatePipe,
    RouterModule,
  ],
  providers: [ApiService, AuthenticationService],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ResourceDetailComponent {
  resource: Resource;
  mapLoc: google.maps.LatLngLiteral;
  currentUser: User;
  changeLog: ResourceChangeLog[];
  loading = true;
  contactItems: ContactItem[];
  typeName: string;
  showInfoWindow = false;
  safeVideoLink: SafeResourceUrl;
  safeVideoImgUrl: SafeResourceUrl;

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
    public router: Router,
    private authenticationService: AuthenticationService,
    private _sanitizer: DomSanitizer,
  ) {
    effect(() => {
      this.currentUser = this.authenticationService.currentUser();
    });
    this.route.params.subscribe(params => {
      this.loading = true;
      this.safeVideoLink = null;
      this.safeVideoImgUrl = null;

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
            this.safeVideoLink = this._sanitizer.bypassSecurityTrustResourceUrl(
              'https://img.youtube.com/vi/' + resource.video_code + '/hqdefault.jpg',
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

  loadMapLocation() {
    afterNextRender(() => {
      if (this.resource && this.resource.hasCoords() && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(p => {
          this.mapLoc = {
            lat: p.coords.latitude,
            lng: p.coords.longitude,
          };
        });
      }
    });
  }

  goPhone($event: MouseEvent) {
    afterNextRender(() => {
      $event.preventDefault();
      if (this.resource && this.resource.phone) {
        location.href = `tel://${this.resource.phone}`;
      }
    });
  }

  goWebsite($event: MouseEvent) {
    afterNextRender(() => {
      $event.preventDefault();
      if (this.resource && this.resource.website) {
        window.open(this.resource.website, '_blank');
      }
    });
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
