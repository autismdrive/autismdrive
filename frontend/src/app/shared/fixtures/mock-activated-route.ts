import {ActivatedRoute, convertToParamMap, Params, UrlSegment} from '@angular/router';
import {mockResource} from '@app/shared/fixtures/mock-resource';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {of} from 'rxjs';

export const mockParamsWithUserId = {studyId: mockUser.id};
export const mockParamsWithStudyId = {studyId: mockStudy.id};
export const mockParamsWithResourceId = {studyId: mockResource.id};
export const mockParamsWithCategoryName = {category: 'Supports_with_Living'};

/**
 * Returns a Mock Activated Route with the given configuration
 *
 * @param {Params} queryParams
 * @param {Params} params
 * @param {Params} path
 * @param {Params} pathFromRoot
 */
export const makeMockActivatedRoute = (
  queryParams?: Params,
  params?: Params,
  path?: string,
  pathFromRoot?: ActivatedRoute[],
) => {
  queryParams = queryParams || {};
  params = params || {};
  pathFromRoot = pathFromRoot || [this];

  return {
    snapshot: {
      queryParamMap: convertToParamMap(queryParams),
      queryParams: queryParams,
      paramMap: convertToParamMap(params),
      params: params,
      url: new UrlSegment(path, params) || undefined,
    },
    queryParamMap: of(convertToParamMap(queryParams)),
    queryParams: of(queryParams),
    paramMap: of(convertToParamMap(params)),
    params: of(params),
    pathFromRoot: pathFromRoot,
  };
};

/** Mock Activated Route for User Admin Details */
export const mockUserDetailsRoute = makeMockActivatedRoute({}, mockParamsWithUserId, 'admin/user/:userId');

/** Mock Activated Route for Study */
export const mockStudyDetailsRoute = makeMockActivatedRoute({}, mockParamsWithStudyId, 'study/:studyId');

/** Mock Activated Route for Study Editing Form */
export const mockStudyEditRoute = makeMockActivatedRoute({}, mockParamsWithStudyId, 'study/edit/:studyId');

/** Mock Activated Route for Studies Page */
export const mockStudiesRoute = makeMockActivatedRoute(
  {},
  {studyStatus: 'study_in_progress', age: 'school'},
  'studies/:studyStatus/:age',
);

/** Mock Activated Route for Resource Details screen */
export const mockResourceDetailsRoute = makeMockActivatedRoute({}, mockParamsWithResourceId, 'resource/:resourceId');

/** Mock Activated Route for Resource Editing Form */
export const mockResourceEditRoute = makeMockActivatedRoute({}, mockParamsWithResourceId, 'resource/edit/:resourceId');

/** Mock Activated Route for COVID-19 Resource */
export const mockCovidRoute = makeMockActivatedRoute({}, mockParamsWithCategoryName, 'covid19-resources/:category');

/** Mock Activated Route for Flow Complete Screen */
export const mockFlowCompleteRoute = makeMockActivatedRoute({}, {}, 'flow/complete');

/** Mock Activated Route for Resource Search Screen */
export const mockSearchQueryRoute = makeMockActivatedRoute({}, {}, 'search');

/** Mock Activated Route for User Profile Screen */
export const mockProfileRoute = makeMockActivatedRoute({meta: true}, {}, 'profile');
