import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@app/_services/api/api.service';
import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockActivatedRouteWithStudyId} from '@util/testing/fixtures/mock-activated-route';
import {mockInvestigator} from '@util/testing/fixtures/mock-investigator';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {mockStudyInvestigator} from '@util/testing/fixtures/mock-study-investigator';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {StudyDetailComponent} from './study-detail.component';

describe('StudyDetailComponent', () => {
  let component: StudyDetailComponent;
  let fixture: MockedComponentFixture<StudyDetailComponent>;

  beforeEach(() => {
    return MockBuilder(StudyDetailComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule)
      .keep(MaterialModule)
      .mock(ApiService, {
        getStudy: jest.fn().mockReturnValue(of(mockStudy)),
        updateInvestigator: jest.fn().mockReturnValue(of(mockInvestigator)),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .provide({provide: ActivatedRoute, useValue: mockActivatedRouteWithStudyId})
      .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {si: mockStudyInvestigator},
      });
  });

  beforeEach(() => {
    fixture = MockRender(StudyDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
