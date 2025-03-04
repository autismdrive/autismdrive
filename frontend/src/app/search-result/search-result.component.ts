/// <reference types="google.maps" />
import {NgClass, NgIf} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatTooltipModule} from '@angular/material/tooltip';
import {RouterModule} from '@angular/router';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {EventDateComponent} from '@app/event-date/event-date.component';
import {FavoriteResourceButtonComponent} from '@app/favorite-resource-button/favorite-resource-button.component';
import {LastUpdatedDateComponent} from '@app/last-updated-date/last-updated-date.component';
import {TypeIconComponent} from '@app/type-icon/type-icon.component';
import {Hit} from '@models/query';
import {StudyStatus} from '@models/study';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {MarkdownModule} from 'ngx-markdown';

@Component({
  standalone: true,
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss'],
  imports: [
    DetailsLinkComponent,
    EventDateComponent,
    FavoriteResourceButtonComponent,
    FlexModule,
    LastUpdatedDateComponent,
    MarkdownModule,
    MatButtonModule,
    MatIconModule,
    MatTooltipModule,
    NgClass,
    NgIf,
    RouterModule,
    TypeIconComponent,
  ],
})
export class SearchResultComponent {
  @Input() hit: Hit;
  @Input() mapLoc: google.maps.LatLngLiteral;
  @Input() currentUser: User;

  hover = false;

  constructor() {}

  get isPastEvent(): boolean {
    return !!(this.hit.date && new Date(this.hit.date) < new Date() && this.hit.post_event_description);
  }

  isEnrolling(status: string) {
    return status === StudyStatus.currently_enrolling;
  }

  statusKey() {
    if (this.hit && this.hit.status) {
      const vals = Object.values(StudyStatus);
      const keys = Object.keys(StudyStatus);
      for (let i = 0; i < vals.length; i++) {
        if (vals[i] === this.hit.status) {
          return keys[i].replace(/_/g, '-');
        }
      }
    }
  }
}
