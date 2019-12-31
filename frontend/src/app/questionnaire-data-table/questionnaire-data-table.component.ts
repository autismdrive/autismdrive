import {Component, Input, OnChanges} from '@angular/core';
import {snakeToUpperCase} from '../../util/snakeToUpper';
import {QuestionnaireDataSource} from '../_models/questionnaire_data_source';
import {TableInfo} from '../_models/table_info';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-questionnaire-data-table',
  templateUrl: './questionnaire-data-table.component.html',
  styleUrls: ['./questionnaire-data-table.component.scss']
})
export class QuestionnaireDataTableComponent implements OnChanges {
  @Input()
  questionnaire_info: TableInfo;
  selected_info: TableInfo;

  dataSource: QuestionnaireDataSource;
  displayedColumns = [];
  columnNames = [];


  constructor(
    private api: ApiService,
  ) {
  }

  get snakeToUpperCase() {
    return snakeToUpperCase;
  }

  ngOnChanges() {
    this.selected_info = this.questionnaire_info;
    this.changeTable(this.selected_info);
  }

  changeTable(table_info) {
    this.selected_info = table_info;
    this.dataSource = new QuestionnaireDataSource(this.api);
    this.dataSource.loadQuestionnaires(this.selected_info.table_name);
    this.load_columns();
  }

  load_columns() {
    this.displayedColumns = [];
    this.columnNames = [];
    this.api
      .getQuestionnaireListMeta(this.selected_info.table_name)
      .subscribe(
      result => {
        for (const column of result['fields']) {
          if (!this.displayedColumns.includes(column.name)) {
            this.displayedColumns.push({'name': column.name, 'type': column.type});
          }
          if (!this.columnNames.includes(column.name)) {
            this.columnNames.push(column.name);
          }
        }
      }
    );
  }

  format_element(element, column) {
    if (column.type === 'DATETIME') {
      return new Date(element[column.name]).toUTCString();
    } else {
      return element[column.name];
    }
  }

  exportQ(info) {
    this.api.exportQuestionnaire(info.table_name).subscribe(response => {
      console.log('data', response);
      const filename = response.headers.get('x-filename');
      const blob = new Blob([response.body], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});

      const url = URL.createObjectURL(blob);
      const a: HTMLAnchorElement = document.createElement('a') as HTMLAnchorElement;

      a.href = url;
      a.download = filename;
      window.document.body.appendChild(a);
      a.click();
      window.document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }
}
