import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ProfileComponent} from './profile.component';

describe('ProfileComponent', () => {
  let component: ProfileComponent;
  let fixture: MockedComponentFixture<ProfileComponent>;

  beforeEach(() => {
    return MockBuilder(ProfileComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ProfileComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
