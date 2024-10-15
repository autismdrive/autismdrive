import {Component, Input} from '@angular/core';
import {Step} from '@models/step';
import {User} from '@models/user';

@Component({
  selector: 'app-questionnaire-step',
  templateUrl: './questionnaire-step.component.html',
  styleUrls: ['./questionnaire-step.component.scss'],
})
export class QuestionnaireStepComponent {
  @Input() user: User;
  step: Step;

  constructor() {}
}
