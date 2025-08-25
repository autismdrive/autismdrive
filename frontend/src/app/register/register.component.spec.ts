import {ActivatedRoute} from '@angular/router';
import {customFormlyConfig} from '@app/app.config';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {LOCAL_STORAGE} from '@app/tokens';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
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
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
      .mock(ApiService, {addUser: jest.fn().mockReturnValue(of(mockUser))})
      .mock(GoogleAnalyticsService, {})
      .provide({provide: LOCAL_STORAGE, useValue: globalThis.localStorage})
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
