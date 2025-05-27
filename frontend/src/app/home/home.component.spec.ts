import {signal} from '@angular/core';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@services/api/api.service';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockAppEnvironment} from '@app/shared/fixtures/mock-app-environment';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {HomeComponent} from './home.component';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: MockedComponentFixture<HomeComponent>;

  beforeEach(() => {
    return MockBuilder(HomeComponent)
      .keep(RouterModule)
      .mock(AppEnvironmentService, {props: signal(mockAppEnvironment)})
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({}, {}, '/home')})
      .mock(ApiService, {
        getStudiesByStatus: jest.fn().mockReturnValue(of([mockStudy])),
      });
  });

  beforeEach(() => {
    fixture = MockRender(HomeComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
