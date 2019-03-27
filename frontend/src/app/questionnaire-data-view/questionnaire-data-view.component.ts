import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ApiService } from '../_services/api/api.service';

@Component({
  selector: 'app-questionnaire-data-view',
  templateUrl: './questionnaire-data-view.component.html',
  styleUrls: ['./questionnaire-data-view.component.scss']
})
export class QuestionnaireDataViewComponent implements OnInit {
  questionnaire_names: any;
  currentQuestionnaire: string;

  mobileQuery: MediaQueryList;
  private _mobileQueryListener: () => void;
  sidebarOpen = true;

  constructor(
    private api: ApiService,
    changeDetectorRef: ChangeDetectorRef,
    media: MediaMatcher
  ) {
    // We will change the display slightly based on mobile vs desktop
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
  }

  ngOnInit() {
    this.api.getQuestionnaireNames().subscribe(
      file_names => {
        this.questionnaire_names = file_names;
      }
    );
  }

  selectQuestionnaire(qn: string) {
    this.currentQuestionnaire = qn;
    this.sidebarOpen = false;
    return this.currentQuestionnaire;
  }

  snakeToUpperCase(s) {
    return s.replace(/([-_][a-z]|^[a-z])/ig, ($1) => {
      return $1.toUpperCase()
        .replace('-', ' ')
        .replace('_', ' ');
    });
  }

}
