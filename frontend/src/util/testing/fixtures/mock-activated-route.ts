import {convertToParamMap} from '@angular/router';
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

// Mock Activated Route for User Admin Details
export const mockActivatedRouteWithUserId = makeMockActivatedRoute({}, mockParamsWithStudyId, [
  {path: 'admin/user/:userId'},
]);

// Mock Activated Route for Portal Event
export const mockActivatedRouteWithStudyId = makeMockActivatedRoute({}, mockParamsWithStudyId, [
  {path: 'study/:study'},
]);

// Mock Activated Route for Studies Page
export const mockActivatedRouteForStudies = makeMockActivatedRoute(
  {},
  {studyStatus: 'study_in_progress', age: 'school'},
  [{path: 'studies/:studyStatus/:age'}],
);

export const mockCovidRouteWithCategoryName = makeMockActivatedRoute({}, mockParamsWithCategoryName, [
  {path: 'covid19-resources/:category'},
]);

export const mockFlowCompleteRoute = makeMockActivatedRoute({}, {}, [{path: 'flow/complete'}]);

export const mockSearchQueryRoute = makeMockActivatedRoute({}, {}, [{path: 'search'}]);

export const mockProfileRoute = makeMockActivatedRoute({meta: true}, {}, [{path: 'profile'}]);
