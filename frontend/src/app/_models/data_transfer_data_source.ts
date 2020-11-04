import {CollectionViewer} from '@angular/cdk/collections';
import {DataSource} from '@angular/cdk/table';
import {BehaviorSubject, Observable} from 'rxjs';
import {ApiService} from '../_services/api/api.service';
import {DataTransferLog} from './data_transfer_log';

export class DataTransferDataSource implements DataSource<DataTransferLog> {

  private logSubject = new BehaviorSubject<DataTransferLog[]>([]);
  public logs$ = this.logSubject.asObservable();
  private countSubject = new BehaviorSubject<number>(0);
  public count$ = this.countSubject.asObservable();
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();

  constructor(
    private api: ApiService
  ) {
  }

  connect(collectionViewer: CollectionViewer): Observable<DataTransferLog[]> {
    return this.logSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.logSubject.complete();
    this.loadingSubject.complete();
    this.countSubject.complete();
  }

  loadLogs(pageNumber = 0, pageSize = 10) {
    this.loadingSubject.next(true);
    this.api.getDataTransferLogs(pageNumber, pageSize)
      .subscribe(results => {
          this.logSubject.next(results.items);
          this.countSubject.next(results.total);
          this.loadingSubject.next(false);
        },
        error1 => {
          this.logSubject.next(null);
          this.countSubject.next(0);
          this.loadingSubject.next(false);
        });
  }
}
