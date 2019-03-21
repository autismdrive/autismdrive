import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { QuestionnaireDataSource } from '../_models/questionnaire_data_source';

@Component({
  selector: 'app-questionnaire-data-table',
  templateUrl: './questionnaire-data-table.component.html',
  styleUrls: ['./questionnaire-data-table.component.scss']
})
export class QuestionnaireDataTableComponent implements OnInit {
  @Input()
  questionnaire_name: string;

  dataSource: QuestionnaireDataSource;
  displayedColumns = [];

  constructor(
    private api: ApiService
  ) { }

  ngOnInit() {
    this.dataSource = new QuestionnaireDataSource(this.api);
    this.dataSource.loadQuestionnaires(this.questionnaire_name);
    this.load_columns();
  }

  load_columns() {
    this.api.getQuestionnaireList(this.questionnaire_name).subscribe(
      result => {
        for (let field in result[0]) {
          this.displayedColumns.push(field);
        }
      }
    )
  }

  snakeToUpperCase(s) {
    return s.replace(/([-_][a-z]|^[a-z])/ig, ($1) => {
      return $1.toUpperCase()
        .replace('-', ' ')
        .replace('_', ' ');
    });
  }

}
