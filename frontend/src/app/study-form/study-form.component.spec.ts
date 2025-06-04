import {OverlayRef} from '@angular/cdk/overlay';
import {MatSelect, MatSelectModule} from '@angular/material/select';
import {ActivatedRoute, Router} from '@angular/router';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {ApiService} from '@services/api/api.service';
import {mockStudyEditRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockCategory} from '@app/shared/fixtures/mock-category';
import {mockInvestigator} from '@app/shared/fixtures/mock-investigator';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockStudyCategory} from '@app/shared/fixtures/mock-study-category';
import {mockStudyInvestigator} from '@app/shared/fixtures/mock-study-investigator';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {of} from 'rxjs';
import {StudyFormComponent} from './study-form.component';

describe('StudyFormComponent', () => {
  let component: StudyFormComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(StudyFormComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
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
      .mock(DeviceDetectorService)
      .keep(MatSelectModule);
  });

  beforeEach(() => {
    fixture = MockRender(StudyFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
