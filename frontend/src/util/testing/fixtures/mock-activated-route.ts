import {convertToParamMap} from '@angular/router';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {of} from 'rxjs';

export const mockParamsWithStudyId = {study: mockStudy.id};

export const makeMockActivatedRoute = (queryParams?: any, params?: any, url?: any[], pathFromRoot?: any[]) => {
  return {
    snapshot: {
      queryParamMap: convertToParamMap(queryParams || {}),
      queryParams: queryParams || {},
      paramMap: convertToParamMap(params || {}),
      params: params || {},
      url: url || undefined,
    },
    queryParamMap: of(convertToParamMap(queryParams || {})),
    queryParams: of(queryParams || {}),
    paramMap: of(convertToParamMap(params || {})),
    params: of(params || {}),
    pathFromRoot: pathFromRoot || [makeMockActivatedRoute],
  };
};

// Mock Activated Route for Portal Event
export const mockActivatedRouteWithStudyId = makeMockActivatedRoute({}, mockParamsWithStudyId, [
  {path: 'study/:study'},
]);
