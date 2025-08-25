import {signal} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {mockStudiesRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {StudiesComponent} from './studies.component';

describe('StudiesComponent', () => {
  let component: StudiesComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(StudiesComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule)
      .keep(Meta)
      .provide({provide: ActivatedRoute, useValue: mockStudiesRoute})
      .mock(ApiService, {
        getStudiesByAge: jest.fn().mockReturnValue(of([mockStudy])),
        getStudiesByStatus: jest.fn().mockReturnValue(of([mockStudy])),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)});
  });

  beforeEach(() => {
    fixture = MockRender(StudiesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
