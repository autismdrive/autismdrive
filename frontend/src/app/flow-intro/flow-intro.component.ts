import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Flow} from '@models/flow';

@Component({
  selector: 'app-flow-intro',
  templateUrl: './flow-intro.component.html',
  styleUrls: ['./flow-intro.component.scss'],
})
export class FlowIntroComponent {
  @Input()
  flow: Flow;

  @Output()
  next: EventEmitter<any> = new EventEmitter();

  constructor() {}

  continue() {
    this.next.emit();
  }
}
