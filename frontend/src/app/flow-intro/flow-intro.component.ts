import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Flow} from '../_models/flow';

@Component({
  selector: 'app-flow-intro',
  templateUrl: './flow-intro.component.html',
  styleUrls: ['./flow-intro.component.scss'],
})
export class FlowIntroComponent implements OnInit {
  @Input()
  flow: Flow;

  @Output()
  next: EventEmitter<any> = new EventEmitter();

  constructor() {}

  ngOnInit() {}

  continue() {
    this.next.emit();
  }
}
