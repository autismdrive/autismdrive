import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Flow} from '@models/flow';

@Component({
  standalone: true,
  selector: 'app-flow-intro',
  templateUrl: './flow-intro.component.html',
  styleUrls: ['./flow-intro.component.scss'],
})
export class FlowIntroComponent {
  @Input() flow: Flow;
  @Output() next = new EventEmitter<any>();

  constructor() {}

  continue() {
    this.next.emit();
  }
}
