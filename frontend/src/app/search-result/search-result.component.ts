import {Component, Input} from '@angular/core';
import {Hit} from '../_models/query';
import {StudyStatus} from '../_models/study';
import {User} from '../_models/user';
import LatLngLiteral = google.maps.LatLngLiteral;

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss'],
})
export class SearchResultComponent {
  @Input() hit: Hit;
  @Input() mapLoc: LatLngLiteral;
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
