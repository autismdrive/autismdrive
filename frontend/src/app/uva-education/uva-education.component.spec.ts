import {signal} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {mockResource} from '@app/shared/fixtures/mock-resource';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@app/shared/services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {UvaEducationComponent} from './uva-education.component';

describe('UvaEducationComponent', () => {
  let component: UvaEducationComponent;
  let fixture: MockedComponentFixture<UvaEducationComponent>;

  beforeEach(() => {
    return MockBuilder(UvaEducationComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getEducationResources: jest.fn().mockReturnValue(of([mockResource])),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .keep(Meta);
  });

  beforeEach(() => {
    fixture = MockRender(UvaEducationComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
