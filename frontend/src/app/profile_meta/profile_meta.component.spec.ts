import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ProfileMetaComponent} from './profile_meta.component';

describe('MetaComponent', () => {
  let component: ProfileMetaComponent;
  let fixture: MockedComponentFixture<ProfileMetaComponent>;

  beforeEach(() => {
    return MockBuilder(ProfileMetaComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ProfileMetaComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
