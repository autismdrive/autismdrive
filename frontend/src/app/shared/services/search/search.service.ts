import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {GeoBox, Query, QueryProps} from '@app/shared/models/query';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';
import {HitType} from '@models/hit_type';
import {sortMethods} from '@models/sort_method';
import {cloneDeep} from 'lodash-es';
import createClone from 'rfdc';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

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
        return this.loadQuery(queryDict);
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

  loadQuery(queryDict: QueryProps): Query {
    if (queryDict?.hits) {
      return new Query(queryDict);
    }

    return new Query({
      geo_box: undefined,
      words: '',
      ages: [],
      languages: [],
      sort: cloneDeep(sortMethods.DISTANCE.sortQuery),
      start: 0,
      types: HitType.all_resources().map(type => type.name),
    });
  }
}
