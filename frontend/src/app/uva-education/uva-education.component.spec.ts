import {AppModule} from '@app/app.module';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockResource} from '@util/testing/fixtures/mock-resource';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {UvaEducationComponent} from './uva-education.component';
import {Meta} from '@angular/platform-browser';
import {ApiService} from '@app/_services/api/api.service';
import {of} from 'rxjs';

describe('UvaEducationComponent', () => {
  let component: UvaEducationComponent;
  let fixture: MockedComponentFixture<UvaEducationComponent>;

  beforeEach(() => {
    return MockBuilder(UvaEducationComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getEducationResources: jest.fn().mockReturnValue(of([mockResource])),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)})
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
