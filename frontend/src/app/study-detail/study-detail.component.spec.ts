import {signal} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@app/shared/services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockStudyDetailsRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockInvestigator} from '@app/shared/fixtures/mock-investigator';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockStudyInvestigator} from '@app/shared/fixtures/mock-study-investigator';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {StudyDetailComponent} from './study-detail.component';

describe('StudyDetailComponent', () => {
  let component: StudyDetailComponent;
  let fixture: MockedComponentFixture<StudyDetailComponent>;

  beforeEach(() => {
    return MockBuilder(StudyDetailComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule)
      .mock(ApiService, {
        getStudy: jest.fn().mockReturnValue(of(mockStudy)),
        updateInvestigator: jest.fn().mockReturnValue(of(mockInvestigator)),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .provide({provide: ActivatedRoute, useValue: mockStudyDetailsRoute})
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
