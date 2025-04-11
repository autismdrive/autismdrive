import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {mockAppEnvironment} from '@util/testing/fixtures/mock-app-environment';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FooterComponent} from './footer.component';

describe('FooterComponent', () => {
  let component: FooterComponent;
  let fixture: MockedComponentFixture<FooterComponent>;

  beforeEach(() => {
    return MockBuilder(FooterComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AppEnvironmentService, mockAppEnvironment);
  });

  beforeEach(() => {
    fixture = MockRender(FooterComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
