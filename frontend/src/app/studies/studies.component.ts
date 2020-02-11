import {Component, OnInit} from '@angular/core';
import {ApiService} from '../_services/api/api.service';
import {Hit, Query} from '../_models/query';
import {Study, StudyStatus} from '../_models/study';
import {AuthenticationService} from '../_services/api/authentication-service';
import {User} from '../_models/user';

interface StudyStatusObj {
  name: string;
  label: string;
}

@Component({
  selector: 'app-studies',
  templateUrl: './studies.component.html',
  styleUrls: ['./studies.component.scss']
})
export class StudiesComponent implements OnInit {
  query: Query;
  studyStatuses: StudyStatusObj[];
  selectedStatus: StudyStatusObj;
  studyHits: Hit[];
  currentUser: User;

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.studyStatuses = Object.keys(StudyStatus).map(k => {
      return {name: k, label: StudyStatus[k]};
    });

    this.selectedStatus = this.studyStatuses[0];
    this.loadStudies();
  }

  ngOnInit() {
  }

  loadStudies() {
    this.api.getStudies().subscribe(studies => {
      this.studyHits = this._studiesToHits(studies.filter(s => s.status === this.selectedStatus.name))
    })
  }

  selectStatus(status: StudyStatusObj) {
    this.selectedStatus = status;
    this.loadStudies();
  }

   private _studiesToHits(studies: Study[]): Hit[] {
      return studies
        .sort((a, b) => (a.id > b.id) ? 1 : -1)
        .map(s => {
          return new Hit({
            id: s.id,
            type: 'study',
            ages: s.ages,
            title: s.short_title,
            content: s.description,
            description: s.short_description,
            last_updated: s.last_updated,
            highlights: null,
            url: `/study/${s.id}`,
            label: 'Research Studies',
            status: this.studyStatuses.find(stat => stat.name === s.status).label
          });
        });
  }

}
