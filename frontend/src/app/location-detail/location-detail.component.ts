import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Location } from '../_models/location';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-location-detail',
  templateUrl: './location-detail.component.html',
  styleUrls: ['./location-detail.component.scss']
})
export class LocationDetailComponent implements OnInit {
location: Location;

  constructor(private api: ApiService, private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      const locationId = params.locationId ? parseInt(params.locationId, 10) : null;

      if (isFinite(locationId)) {
        this.api.getLocation(locationId).subscribe(location => {
          this.location = location;
        });
      }
    });
  }

  ngOnInit() {
  }

  goPhone($event: MouseEvent) {
    $event.preventDefault();
    if (this.location && this.location.phone) {
      location.href = `tel://${this.location.phone}`;
    }
  }

  goWebsite($event: MouseEvent) {
    $event.preventDefault();
    if (this.location && this.location.website) {
      location.href = this.location.website;
    }
  }

}
