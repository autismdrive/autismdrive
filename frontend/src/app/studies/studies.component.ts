import {Component} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, Router} from '@angular/router';
import {AgeRange} from '@models/hit_type';
import {Hit, Query} from '@models/query';
import {Study, StudyStatus} from '@models/study';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

interface StudyStatusObj {
  name: string;
  label: string;
}

interface AgeObj {
  name: string;
  label: string;
}

@Component({
  selector: 'app-studies',
  templateUrl: './studies.component.html',
  styleUrls: ['./studies.component.scss'],
})
export class StudiesComponent {
  query: Query;
  studyStatuses: StudyStatusObj[];
  selectedStatus: StudyStatusObj;
  selectedAge: AgeObj;
  studyHits: Hit[];
  currentUser: User;
  Ages: AgeObj[];

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private route: ActivatedRoute,
    private router: Router,
    private meta: Meta,
  ) {
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
    this.meta.updateTag(
      {property: 'og:image', content: location.origin + '/assets/studies/hero.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: location.origin + '/assets/studies/hero.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: location.origin + '/assets/studies/hero.jpg'},
      `name='twitter:image'`,
    );
    this.studyStatuses = Object.keys(StudyStatus).map(k => {
      return {name: k, label: StudyStatus[k]};
    });
    this.Ages = Object.keys(AgeRange.labels).map(k => {
      return {name: k, label: AgeRange.labels[k]};
    });
    this.route.params.subscribe(params => {
      if ('studyStatus' in params) {
        this.selectedStatus = this.studyStatuses.find(x => x.name === params['studyStatus']);
        if ('age' in params) {
          this.selectedAge = this.Ages.find(x => x.name === params['age']);
        } else {
          this.selectedAge = undefined;
        }
      } else {
        this.selectedStatus = this.studyStatuses[0];
        this.route.params['studyStatus'] = this.studyStatuses[0].name;
        this.selectedAge = undefined;
        this.router.navigate(['/studies/' + this.studyStatuses[0].name]);
      }
    });
    this.loadStudies();
  }

  loadStudies() {
    if (this.selectedAge) {
      this.api.getStudiesByAge(this.selectedStatus.name, this.selectedAge.name).subscribe(studies => {
        this.studyHits = this._studiesToHits(studies);
      });
    } else {
      this.api.getStudiesByStatus(this.selectedStatus.name).subscribe(studies => {
        this.studyHits = this._studiesToHits(studies);
      });
    }
  }

  selectStatus(status: StudyStatusObj) {
    this.selectedStatus = status;
    this.router.navigate(['/studies/' + status.name]);
    this.loadStudies();
  }

  selectAge(age?: AgeObj) {
    this.selectedAge = age;
    if (age) {
      this.router.navigate(['/studies/' + this.selectedStatus.name + '/' + age.name]);
    } else {
      this.router.navigate(['/studies/' + this.selectedStatus.name]);
    }
    this.loadStudies();
  }

  private _studiesToHits(studies: Study[]): Hit[] {
    return studies.map(s => {
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
        status: this.studyStatuses.find(stat => stat.name === s.status).label,
      });
    });
  }
}
