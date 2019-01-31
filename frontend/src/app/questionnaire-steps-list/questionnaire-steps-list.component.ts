import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { QuestionnaireStep } from '../step';
import { User } from '../user';

@Component({
  selector: 'app-questionnaire-steps-list',
  templateUrl: './questionnaire-steps-list.component.html',
  styleUrls: ['./questionnaire-steps-list.component.scss'],
})
export class QuestionnaireStepsListComponent implements OnInit {
  @Input() user: User;
  @Input() stepNames: string[];
  steps: QuestionnaireStep[] = [];

  constructor(private api: ApiService) {
  }

  ngOnInit() {
    if (this.stepNames && (this.stepNames.length > 0)) {
      this.stepNames.forEach((stepName, i) => {
        this.api.getQuestionnaireMeta(stepName).subscribe(q => {
          const stepInfo = q.get_meta.table;

          this.steps[i] = new QuestionnaireStep({
            name: stepName,
            label: stepInfo.label,
            description: stepInfo.description
          });
        });
      });
    }
  }

}
