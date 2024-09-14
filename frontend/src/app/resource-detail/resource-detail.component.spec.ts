import {AppModule} from '@app/app.module';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ResourceDetailComponent} from './resource-detail.component';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@app/_services/api/api.service';
import {DomSanitizer} from '@angular/platform-browser';
import {of} from 'rxjs';

describe('ResourceDetailComponent', () => {
  let component: ResourceDetailComponent;
  let fixture: MockedComponentFixture<ResourceDetailComponent>;

  beforeEach(() => {
    return MockBuilder(ResourceDetailComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {getResourceChangeLog: jest.fn().mockReturnValue(of([]))})
      .keep(ActivatedRoute)
      .keep(RouterModule)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(DomSanitizer);
  });

  beforeEach(() => {
    fixture = MockRender(ResourceDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
