import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ApiService } from '../_services/api/api.service';
import { snakeToUpperCase } from '../../util/snakeToUpper';

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

  exportAll() {
    console.log('clicking the button for export all');
    this.api.exportQuestionnaire( 'all').subscribe( response => {
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

  get snakeToUpperCase() { return snakeToUpperCase; }
}
