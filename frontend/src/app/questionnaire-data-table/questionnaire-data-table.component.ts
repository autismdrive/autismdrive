import { Component, Input, OnChanges } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { QuestionnaireDataSource } from '../_models/questionnaire_data_source';
import { snakeToUpperCase } from '../../util/snakeToUpper';

@Component({
  selector: 'app-questionnaire-data-table',
  templateUrl: './questionnaire-data-table.component.html',
  styleUrls: ['./questionnaire-data-table.component.scss']
})
export class QuestionnaireDataTableComponent implements OnChanges {
  @Input()
  questionnaire_name: string;

  dataSource: QuestionnaireDataSource;
  displayedColumns = [];


  constructor(
    private api: ApiService,
  ) {}

  ngOnChanges() {
    this.dataSource = new QuestionnaireDataSource(this.api);
    this.dataSource.loadQuestionnaires(this.questionnaire_name);
    this.load_columns();
  }

  load_columns() {
    this.displayedColumns = [];
    this.api.getQuestionnaireListMeta(this.questionnaire_name).subscribe(
      result => {
        for (let fieldIndex in result['fields']) {
          if (!this.displayedColumns.includes(result['fields'][fieldIndex].name)){
            this.displayedColumns.push(result['fields'][fieldIndex].name);
          }
        }
      }
    );
  }

  get snakeToUpperCase(){ return snakeToUpperCase }
}
