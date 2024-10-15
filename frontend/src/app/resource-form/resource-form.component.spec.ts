import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockResource} from '@util/testing/fixtures/mock-resource';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {of} from 'rxjs';
import {ResourceFormComponent} from './resource-form.component';

describe('ResourceFormComponent', () => {
  let component: ResourceFormComponent;
  let fixture: MockedComponentFixture<ResourceFormComponent>;

  beforeEach(() => {
    return MockBuilder(ResourceFormComponent, AppModule)
      .keep(FormlyModule.forRoot())
      .keep(FormsModule)
      .keep(MaterialModule)
      .keep(ReactiveFormsModule)
      .mock(ApiService, {
        getCategoryTree: jest.fn().mockReturnValue(of([])),
        deleteResource: jest.fn().mockReturnValue(of(mockResource)),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(DeviceDetectorService)
      .keep(ActivatedRoute)
      .keep(RouterModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ResourceFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
