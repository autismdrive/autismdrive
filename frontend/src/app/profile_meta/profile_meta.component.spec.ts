import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {ProfileMetaComponent} from './profile_meta.component';

describe('MetaComponent', () => {
  let component: ProfileMetaComponent;
  let fixture: MockedComponentFixture<ProfileMetaComponent>;

  beforeEach(() => {
    return MockBuilder(ProfileMetaComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ProfileMetaComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
