import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {mockAdminNote} from '@util/testing/fixtures/mock-admin-note';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {RegisterDialogComponent} from './register-dialog.component';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {of} from 'rxjs';

describe('RegisterDialogComponent', () => {
  let component: RegisterDialogComponent;
  let fixture: MockedComponentFixture<RegisterDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RegisterDialogComponent, AppModule)
      .keep(RouterModule)
      .keep(ActivatedRoute)
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
