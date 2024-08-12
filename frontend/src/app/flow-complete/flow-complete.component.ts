import {Component, Input} from '@angular/core';
import {Router} from '@angular/router';
import {Flow} from '@models/flow';
import {ParticipantRelationship} from '@models/participantRelationship';

@Component({
  selector: 'app-flow-complete',
  templateUrl: './flow-complete.component.html',
  styleUrls: ['./flow-complete.component.scss'],
})
export class FlowCompleteComponent {
  @Input()
  flow: Flow;

  constructor(private router: Router) {}

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
