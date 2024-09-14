import {convertToParamMap} from '@angular/router';
import {Covid19Categories} from '@models/hit_type';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {of} from 'rxjs';

export const mockParamsWithStudyId = {study: mockStudy.id};
export const mockParamsWithCategoryName = {category: 'Supports_with_Living'};

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

export const mockCovidRouteWithCategoryName = makeMockActivatedRoute({}, mockParamsWithCategoryName, [
  {path: 'covid19-resources/:category'},
]);

export const mockFlowCompleteRoute = makeMockActivatedRoute({}, {}, [{path: 'flow/complete'}]);

export const mockSearchQueryRoute = makeMockActivatedRoute({}, {}, [{path: 'search'}]);
