import {ActivatedRoute, RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {StudyStatus} from '@models/study';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockActivatedRouteForStudies} from '@util/testing/fixtures/mock-activated-route';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {StudiesComponent} from './studies.component';
import {Meta} from '@angular/platform-browser';
import {of} from 'rxjs';

describe('StudiesComponent', () => {
  let component: StudiesComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(StudiesComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule)
      .keep(Meta)
      .provide({provide: ActivatedRoute, useValue: mockActivatedRouteForStudies})
      .mock(ApiService, {
        getStudiesByAge: jest.fn().mockReturnValue(of([mockStudy])),
        getStudiesByStatus: jest.fn().mockReturnValue(of([mockStudy])),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)});
  });

  beforeEach(() => {
    fixture = MockRender(StudiesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
