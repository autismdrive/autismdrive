import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Query} from 'src/app/_models/query';
import createClone from 'rfdc';
import {ConfigService} from '../config/config.service';


@Injectable({providedIn: 'root'})
export class SearchService {
  public currentQuery: Observable<Query>;
  query_url = '/api/search/resources';
  private _querySubject: BehaviorSubject<Query>;

  constructor(private _http: HttpClient, private config: ConfigService) {
    const queryDict = JSON.parse(localStorage.getItem('currentQuery'));
    if (queryDict) {
      this._querySubject = new BehaviorSubject<Query>(new Query(queryDict));
    } else {
      this._querySubject = new BehaviorSubject<Query>(null);
    }
    this.currentQuery = this._querySubject.asObservable();
  }

  public get currentQueryValue(): Query {
    return this._querySubject.value;
  }

  search(query: Query): Observable<Query> {
    const url = this.config.apiUrl + this.query_url;
    return this._http
      .post<any>(url, query)
      .pipe(map(queryDict => {
        console.log('queryDict', queryDict);
        return this._loadQuery(queryDict);
      }));
  }

  mapSearch(query: Query, mapDataOnly = true): Observable<Query> {
    const mapQuery = createClone({circles: true})(query);
    mapQuery.size = 200;
    mapQuery.map_data_only = mapDataOnly;
    return this.search(mapQuery);
  }

  reset() {
    localStorage.removeItem('currentQuery');
    this._querySubject.next(null);
  }

  private _loadQuery(queryDict): Query {
    if (queryDict && queryDict.hits) {
      const query = new Query(queryDict);
      localStorage.setItem('currentQuery', JSON.stringify(queryDict));
      this._querySubject.next(query);
      this.currentQuery = this._querySubject.asObservable();
      return query;
    }
  }
}
