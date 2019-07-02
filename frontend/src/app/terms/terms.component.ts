import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ParticipantRelationship } from '../_models/participantRelationship';


@Component({
  selector: 'app-terms',
  templateUrl: './terms.component.html',
  styleUrls: ['./terms.component.scss']
})
export class TermsComponent implements OnInit {

  @Input() relationship: ParticipantRelationship;

  @Input() preview: boolean;

  @Output() next: EventEmitter<any> = new EventEmitter();

  constructor(
    private router: Router,
    private route: ActivatedRoute,
  ) {
    this.route.params.subscribe(params => {
      if ('relationship' in params) {
        this.relationship = params['relationship'];
        this.preview = true;
      }
    });
  }

  ngOnInit() {
  }

  goProfile($event) {
    $event.preventDefault();
    this.router.navigate(['profile']);
  }

  continue() {
    this.next.emit();
  }
}
