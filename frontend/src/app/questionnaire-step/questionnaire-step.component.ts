import { Component, OnInit, Input } from '@angular/core';
import { QuestionnaireStep } from '../step';
import { User } from '../user';

@Component({
  selector: 'app-questionnaire-step',
  templateUrl: './questionnaire-step.component.html',
  styleUrls: ['./questionnaire-step.component.scss']
})
export class QuestionnaireStepComponent implements OnInit {
  @Input() user: User;
  step: QuestionnaireStep;

  constructor() { }

  ngOnInit() {
  }

}
