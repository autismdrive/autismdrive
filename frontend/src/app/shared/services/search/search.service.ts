import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import createClone from 'rfdc';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {GeoBox, Query} from '@app/shared/models/query';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';

@Injectable({providedIn: 'root'})
export class SearchService {
  query_url = '/api/search/resources';

  constructor(
    private _http: HttpClient,
    private config: AppEnvironmentService,
  ) {}

  search(query: Query): Observable<Query> {
    const url = this.config.apiUrl + this.query_url;
    return this._http.post<any>(url, query).pipe(
      map(queryDict => {
        return this._loadQuery(queryDict);
      }),
    );
  }

  mapSearch(query: Query, geoBox?: GeoBox): Observable<Query> {
    const mapQuery = createClone({circles: true})(query);
    mapQuery.geo_box = geoBox;
    mapQuery.map_data_only = true;
    mapQuery.size = 300;
    return this.search(mapQuery);
  }

  private _loadQuery(queryDict): Query {
    if (queryDict && queryDict.hits) {
      const query = new Query(queryDict);
      return query;
    }
  }
}
