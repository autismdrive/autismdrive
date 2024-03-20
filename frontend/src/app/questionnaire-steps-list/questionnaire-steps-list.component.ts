import {Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {Flow} from '../_models/flow';
import {Step} from '../_models/step';
import {ApiService} from '../_services/api/api.service';

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

  constructor(private api: ApiService) {}

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
