import {CollectionViewer} from '@angular/cdk/collections';
import {DataSource} from '@angular/cdk/table';
import {BehaviorSubject, Observable} from 'rxjs';
import {ApiService} from '../_services/api/api.service';
import {Step} from './step';

export class QuestionnaireDataSource implements DataSource<Step> {

  private stepSubject = new BehaviorSubject<any>([]);
  private countSubject = new BehaviorSubject<number>(0);
  private loadingSubject = new BehaviorSubject<boolean>(false);

  constructor(private api: ApiService) {
  }

  connect(collectionViewer: CollectionViewer): Observable<Step[]> {
    return this.stepSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.stepSubject.complete();
    this.loadingSubject.complete();
    this.countSubject.complete();
  }

  loadQuestionnaires(questionnaire_name) {
    this.loadingSubject.next(true);
    this.api.getQuestionnaireList(questionnaire_name).subscribe(
      results => {
        this.stepSubject.next(results);
      }
    );
  }
}
