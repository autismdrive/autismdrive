import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';

@Component({
  selector: 'app-admin-home',
  templateUrl: './admin-home.component.html',
  styleUrls: ['./admin-home.component.scss']
})
export class AdminHomeComponent implements OnInit {
  questionnaire_names = [];

  constructor(
    private api: ApiService
  ) { }

  ngOnInit() {
    this.api.getQuestionnaireNames().subscribe(
      file_names => {
        this.questionnaire_names = file_names;
      }
    )
  }

}
