import {CommonModule} from '@angular/common';
import {Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {MatListModule} from '@angular/material/list';
import {Flow} from '@models/flow';
import {Step} from '@models/step';
import {FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-questionnaire-steps-list',
  templateUrl: './questionnaire-steps-list.component.html',
  styleUrls: ['./questionnaire-steps-list.component.scss'],
  imports: [CommonModule, MatListModule, MatIconModule, FlexModule],
})
export class QuestionnaireStepsListComponent implements OnInit, OnChanges {
  @Input() flow: Flow;
  @Input() stepIndex: number;
  @Output()
  stepSelected = new EventEmitter<Step>();
  stepName: string;

  constructor() {}

  ngOnChanges(changes: SimpleChanges): void {
    this.stepName = this.flow.steps[this.stepIndex].name;
  }

  ngOnInit() {
    this.stepName = this.flow.steps[this.stepIndex].name;
  }

  selectStep(step: Step) {
    this.stepName = step.name;
    this.stepSelected.emit(step);
  }
}
