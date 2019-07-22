import { User } from './user';
import { DataSource } from '@angular/cdk/table';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';
import { ApiService } from '../_services/api/api.service';
import { CollectionViewer } from '@angular/cdk/collections';
import { Observable } from 'rxjs/internal/Observable';
import {ExportLog} from './export_log';

export class ExportLogDataSource implements DataSource<ExportLog> {

  private logSubject = new BehaviorSubject<ExportLog[]>([]);
  private countSubject = new BehaviorSubject<number>(0);
  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public count$ = this.countSubject.asObservable();

  constructor(
    private api: ApiService
  ) {}

  connect(collectionViewer: CollectionViewer): Observable<ExportLog[]> {
    return this.logSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.logSubject.complete();
    this.loadingSubject.complete();
    this.countSubject.complete();
  }

  loadLogs(pageNumber = 0, pageSize = 10) {
    this.loadingSubject.next(true);
    this.api.getExportLogs(pageNumber, pageSize)
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
