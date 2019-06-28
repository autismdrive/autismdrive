import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Resource } from '../_models/resource';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-resource-detail',
  templateUrl: './resource-detail.component.html',
  styleUrls: ['./resource-detail.component.scss']
})
export class ResourceDetailComponent implements OnInit {
  resource: Resource;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute
  ) {
    this.route.params.subscribe(params => {
      const resourceId = params.resourceId ? parseInt(params.resourceId, 10) : null;
      if (this.route.snapshot.data['title'] == 'Event Details') {
        if (isFinite(resourceId)) {
          this.api.getEvent(resourceId).subscribe(resource => {
            this.resource = resource;
          });
        }
      } else if (this.route.snapshot.data['title'] == 'Location Details') {
        if (isFinite(resourceId)) {
          this.api.getLocation(resourceId).subscribe(resource => {
            this.resource = resource;
          });
        }
      } else if (this.route.snapshot.data['title'] == 'Resource Details') {
        if (isFinite(resourceId)) {
          this.api.getResource(resourceId).subscribe(resource => {
            this.resource = resource;
          });
        }
      }
    });
  }

  ngOnInit() {
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
