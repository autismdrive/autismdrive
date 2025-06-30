import {signal} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatSelectModule} from '@angular/material/select';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {customFormlyConfig} from '@app/app.config';
import {mockResourceEditRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockResource} from '@app/shared/fixtures/mock-resource';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {of} from 'rxjs';
import {ResourceFormComponent} from './resource-form.component';

describe('ResourceFormComponent', () => {
  let component: ResourceFormComponent;
  let fixture: MockedComponentFixture<ResourceFormComponent>;

  beforeEach(() => {
    return MockBuilder(ResourceFormComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
      .keep(FormsModule)
      .keep(ReactiveFormsModule)
      .mock(ApiService, {
        getCategoryTree: jest.fn().mockReturnValue(of([])),
        deleteResource: jest.fn().mockReturnValue(of(mockResource)),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(DeviceDetectorService)
      .provide({
        provide: ActivatedRoute,
        useValue: mockResourceEditRoute,
      })
      .keep(RouterModule)
      .keep(MatSelectModule);
  });

  beforeEach(() => {
    fixture = MockRender(ResourceFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
    window.scrollTo = jest.fn();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
