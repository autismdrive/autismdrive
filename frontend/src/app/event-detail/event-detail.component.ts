import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Event } from '../_models/event';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-event-detail',
  templateUrl: './event-detail.component.html',
  styleUrls: ['./event-detail.component.scss']
})
export class EventDetailComponent implements OnInit {
  event: Event;

  constructor(private api: ApiService, private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      const eventId = params.eventId ? parseInt(params.eventId, 10) : null;

      if (isFinite(eventId)) {
        this.api.getEvent(eventId).subscribe(event => {
          this.event = event;
        });
      }
    });
  }

  ngOnInit() {
  }

  goPhone($event: MouseEvent) {
    $event.preventDefault();
    if (this.event && this.event.phone) {
      location.href = `tel://${this.event.phone}`;
    }
  }

  goWebsite($event: MouseEvent) {
    $event.preventDefault();
    if (this.event && this.event.website) {
      location.href = this.event.website;
    }
  }
}
