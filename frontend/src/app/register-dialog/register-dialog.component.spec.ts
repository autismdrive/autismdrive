import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {RouterModule} from '@angular/router';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {RegisterDialogComponent} from './register-dialog.component';

describe('RegisterDialogComponent', () => {
  let component: RegisterDialogComponent;
  let fixture: MockedComponentFixture<RegisterDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RegisterDialogComponent)
      .keep(RouterModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {addUser: jest.fn().mockReturnValue(of(mockUser))})
      .mock(GoogleAnalyticsService)
      .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {displaySurvey: true},
      });
  });

  beforeEach(() => {
    fixture = MockRender(RegisterDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
