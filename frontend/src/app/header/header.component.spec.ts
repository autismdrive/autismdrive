import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {ActivatedRoute} from '@angular/router';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {makeMockActivatedRoute} from '@fixtures/mock-activated-route';
import {ApiService} from '@services/api/api.service';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {HeaderComponent} from './header.component';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(HeaderComponent)
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({}, {}, '/home')})
      .mock(ApiService, {})
      .mock(AppEnvironmentService, {mirroring: false});
  });

  beforeEach(() => {
    fixture = MockRender(HeaderComponent, {currentUser: mockUser}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
