import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { ParticipantRelationship } from '../_models/participantRelationship';

@Component({
  selector: 'app-terms',
  templateUrl: './terms.component.html',
  styleUrls: ['./terms.component.scss']
})
export class TermsComponent implements OnInit {

  @Input()
  relationship: ParticipantRelationship;

  @Output()
  next: EventEmitter<any> = new EventEmitter();

  constructor(
    private router: Router
  ) { }

  ngOnInit() {
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }

  continue() {
    this.next.emit();
  }
}
