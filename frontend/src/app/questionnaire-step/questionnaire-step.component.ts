import {Component, Input, OnInit} from '@angular/core';
import {Step} from '../_models/step';
import {User} from '../_models/user';

@Component({
  selector: 'app-questionnaire-step',
  templateUrl: './questionnaire-step.component.html',
  styleUrls: ['./questionnaire-step.component.scss'],
})
export class QuestionnaireStepComponent implements OnInit {
  @Input() user: User;
  step: Step;

  constructor() {}

  ngOnInit() {}
}
