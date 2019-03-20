import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { QuestionnaireDataSource } from '../_models/questionnaire_data_source';

@Component({
  selector: 'app-admin-home',
  templateUrl: './admin-home.component.html',
  styleUrls: ['./admin-home.component.scss']
})
export class AdminHomeComponent implements OnInit {
  dataSource: QuestionnaireDataSource;
  displayedColumns = [];

  constructor(
    private api: ApiService
  ) { }

  ngOnInit() {
    this.dataSource = new QuestionnaireDataSource(this.api);
    this.dataSource.loadQuestionnaires('identification_questionnaire');
    this.load_columns();
  }

  load_columns() {
    this.api.getQuestionnaireList('identification_questionnaire').subscribe(
      result => {
        for (let field in result[0]) {
          this.displayedColumns.push(field);
        }
      }
    )
  }

}
