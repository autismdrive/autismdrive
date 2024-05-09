import {MediaMatcher} from '@angular/cdk/layout';
import {ChangeDetectorRef, Component, OnDestroy, OnInit} from '@angular/core';
import {snakeToUpperCase} from '@util/snakeToUpper';
import {TableInfo} from '../_models/table_info';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-questionnaire-data-view',
  templateUrl: './questionnaire-data-view.component.html',
  styleUrls: ['./questionnaire-data-view.component.scss'],
})
export class QuestionnaireDataViewComponent implements OnInit, OnDestroy {
  questionnaire_info: TableInfo[];
  currentQuestionnaire: TableInfo;

  mobileQuery: MediaQueryList;
  sidebarOpen = true;
  private _mobileQueryListener: () => void;

  constructor(private api: ApiService, changeDetectorRef: ChangeDetectorRef, media: MediaMatcher) {
    // We will change the display slightly based on mobile vs desktop
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    // Using addEventListener causes page failures for older Sarafi / webkit / iPhone
    // this.mobileQuery.addEventListener('change', this._mobileQueryListener);
    // tslint:disable-next-line:deprecation
    this.mobileQuery.addListener(this._mobileQueryListener);

    window.addEventListener('resize', this._mobileQueryListener);
  }

  get snakeToUpperCase() {
    return snakeToUpperCase;
  }

  ngOnInit() {
    this.api.getQuestionnaireInfoList().subscribe(info => {
      this.questionnaire_info = info;
    });
  }

  ngOnDestroy(): void {
    // removeEventListener fails on older versions of iOS / Safari / iPhone
    // this.mobileQuery.removeEventListener('change', this._mobileQueryListener);
    // tslint:disable-next-line:deprecation
    this.mobileQuery.removeListener(this._mobileQueryListener);
    window.removeEventListener('resize', this._mobileQueryListener);
  }

  selectQuestionnaire(info: TableInfo) {
    this.currentQuestionnaire = info;
    this.sidebarOpen = false;
    return this.currentQuestionnaire;
  }

  exportAll() {
    console.log('clicking the button for export all');
    this.api.exportQuestionnaire('all').subscribe(response => {
      console.log('data', response);
      const filename = response.headers.get('x-filename');
      const blob = new Blob([response.body], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });

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
