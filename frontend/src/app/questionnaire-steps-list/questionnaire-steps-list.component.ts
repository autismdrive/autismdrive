import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import { ApiService } from '../services/api/api.service';
import {Flow} from '../flow';
import {Step} from '../step';

@Component({
  selector: 'app-questionnaire-steps-list',
  templateUrl: './questionnaire-steps-list.component.html',
  styleUrls: ['./questionnaire-steps-list.component.scss'],
})
export class QuestionnaireStepsListComponent implements OnInit {
  @Input() flow: Flow;

  @Output()
  stepSelected: EventEmitter<Step> = new EventEmitter();

  constructor(private api: ApiService) {
  }

  ngOnInit() {
  }

  selectStep(step: Step) {
    this.stepSelected.emit(step);
  }

}
