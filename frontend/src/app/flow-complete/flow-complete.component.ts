import {Component, Input, OnInit} from '@angular/core';
import {Flow} from '../_models/flow';
import {Router} from '@angular/router';
import {ParticipantRelationship} from '../_models/participantRelationship';

@Component({
  selector: 'app-flow-complete',
  templateUrl: './flow-complete.component.html',
  styleUrls: ['./flow-complete.component.scss']
})
export class FlowCompleteComponent implements OnInit {

  @Input()
  flow: Flow;

  constructor(private router: Router) { }

  ngOnInit() {
  }

  goProfile($event) {
    $event.preventDefault();
    this.router.navigate(['profile']);
  }

  goStudies($event) {
    $event.preventDefault();
    this.router.navigate(['studies']);
  }

  goResources($event) {
    $event.preventDefault();
    this.router.navigate(['search']);
  }

  enrollDependent($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.DEPENDENT]);
  }
}
