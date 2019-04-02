import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Query } from 'src/app/_models/query';
import { environment } from '../../../environments/environment';


@Injectable({ providedIn: 'root' })
export class SearchService {
  private querySubject: BehaviorSubject<Query>;
  public currentQuery: Observable<Query>;
  query_url = `${environment.api}/api/search`;

  constructor(private http: HttpClient) {
    const queryDict = JSON.parse(localStorage.getItem('currentQuery'));
    if (queryDict) {
      this.querySubject = new BehaviorSubject<Query>(new Query(queryDict));
    } else {
      this.querySubject = new BehaviorSubject<Query>(null);
    }
    this.currentQuery = this.querySubject.asObservable();
  }

  public get currentQueryValue(): Query {
    return this.querySubject.value;
  }

  private loadQuery(queryDict): Query {
    if (queryDict && queryDict.hits) {
      const query = new Query(queryDict);

      console.log('query', query);

      localStorage.setItem('currentQuery', JSON.stringify(queryDict));
      this.querySubject.next(query);
      this.currentQuery = this.querySubject.asObservable();
      return query;
    }
  }

  search(query: Query): Observable<Query> {
    return this.http.post<any>(this.query_url, query)
      .pipe(map(queryDict => {
        return this.loadQuery(queryDict);
      }));
  }

  reset() {
    localStorage.removeItem('currentQuery');
    this.querySubject.next(null);
  }
}
