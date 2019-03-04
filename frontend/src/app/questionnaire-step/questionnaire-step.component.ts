import { Component, OnInit, Input } from '@angular/core';
import { User } from '../user';
import {Step} from '../step';

@Component({
  selector: 'app-questionnaire-step',
  templateUrl: './questionnaire-step.component.html',
  styleUrls: ['./questionnaire-step.component.scss']
})
export class QuestionnaireStepComponent implements OnInit {
  @Input() user: User;
  step: Step;

  constructor() { }

  ngOnInit() {
  }

}
