import {ActivatedRoute} from '@angular/router';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {RegisterComponent} from './register.component';

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: MockedComponentFixture<RegisterComponent>;

  beforeEach(() => {
    return MockBuilder(RegisterComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {addUser: jest.fn().mockReturnValue(of(mockUser))})
      .mock(GoogleAnalyticsService, {})
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({}, {}, 'register')});
  });

  beforeEach(() => {
    fixture = MockRender(RegisterComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
