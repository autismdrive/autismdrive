import {ActivatedRoute, Router} from '@angular/router';
import {FormlyConfig} from '@app/app.config';
import {FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {mockStudyEditRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockInvestigator} from '@util/testing/fixtures/mock-investigator';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {mockStudyCategory} from '@util/testing/fixtures/mock-study-category';
import {mockStudyInvestigator} from '@util/testing/fixtures/mock-study-investigator';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {of} from 'rxjs';
import {StudyFormComponent} from './study-form.component';

describe('StudyFormComponent', () => {
  let component: StudyFormComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(StudyFormComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getInvestigators: jest.fn().mockReturnValue(of([mockInvestigator])),
        getCategoryTree: jest.fn().mockReturnValue(of([mockCategory])),
        getStudy: jest.fn().mockReturnValue(of(mockStudy)),
        updateStudyCategories: jest.fn().mockReturnValue(of([mockStudyCategory])),
        addInvestigator: jest.fn().mockReturnValue(of(mockInvestigator)),
        updateStudyInvestigators: jest.fn().mockReturnValue(of(mockStudyInvestigator)),
        addStudy: jest.fn().mockReturnValue(of(mockStudy)),
        updateStudy: jest.fn().mockReturnValue(of(mockStudy)),
        deleteStudy: jest.fn().mockReturnValue(of(mockStudy)),
      })
      .provide({provide: ActivatedRoute, useValue: mockStudyEditRoute})
      .keep(Router)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .mock(DeviceDetectorService);
  });

  beforeEach(() => {
    fixture = MockRender(StudyFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
