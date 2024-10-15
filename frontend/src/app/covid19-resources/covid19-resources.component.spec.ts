import {ActivatedRoute, RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockCovidRouteWithCategoryName} from '@util/testing/fixtures/mock-activated-route';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {Covid19ResourcesComponent} from './covid19-resources.component';

describe('Covid19ResourcesComponent', () => {
  let component: Covid19ResourcesComponent;
  let fixture: MockedComponentFixture<Covid19ResourcesComponent>;

  beforeEach(() => {
    return MockBuilder(Covid19ResourcesComponent, AppModule)
      .keep(RouterModule.forRoot([{path: 'covid19-resources/:category', component: Covid19ResourcesComponent}]), {
        dependency: false,
      })
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getCovid19ResourcesByCategory: jest.fn().mockReturnValue(of([])),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .provide({provide: ActivatedRoute, useValue: mockCovidRouteWithCategoryName});
  });

  beforeEach(() => {
    fixture = MockRender(Covid19ResourcesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
