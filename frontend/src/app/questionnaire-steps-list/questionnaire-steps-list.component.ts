import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ApiService } from '../services/api/api.service';
import { Flow } from '../flow';
import { Step } from '../step';

@Component({
  selector: 'app-questionnaire-steps-list',
  templateUrl: './questionnaire-steps-list.component.html',
  styleUrls: ['./questionnaire-steps-list.component.scss'],
})
export class QuestionnaireStepsListComponent implements OnInit {
  @Input() flow: Flow;
  @Output()
  stepSelected: EventEmitter<Step> = new EventEmitter();
  stepName: string;

  constructor(private api: ApiService) {
  }

  ngOnInit() {
    this.stepName = this.flow.steps[0].name;
  }

  selectStep(step: Step) {
    this.stepName = step.name;
    this.stepSelected.emit(step);
  }

}
