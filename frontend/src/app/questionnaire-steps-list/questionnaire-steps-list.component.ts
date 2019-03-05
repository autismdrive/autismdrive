import { Component, EventEmitter, Input, OnInit, Output, OnChanges, SimpleChanges } from '@angular/core';
import { ApiService } from '../services/api/api.service';
import { Flow } from '../flow';
import { Step } from '../step';

@Component({
  selector: 'app-questionnaire-steps-list',
  templateUrl: './questionnaire-steps-list.component.html',
  styleUrls: ['./questionnaire-steps-list.component.scss'],
})
export class QuestionnaireStepsListComponent implements OnInit, OnChanges {
  @Input() flow: Flow;
  @Input() stepIndex: number;
  @Output()
  stepSelected: EventEmitter<Step> = new EventEmitter();
  stepName: string;

  constructor(private api: ApiService) {
  }

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
