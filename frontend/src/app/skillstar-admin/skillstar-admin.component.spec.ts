import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {SkillstarAdminComponent} from './skillstar-admin.component';

describe('SkillstarAdminComponent', () => {
  let component: SkillstarAdminComponent;
  let fixture: MockedComponentFixture<SkillstarAdminComponent>;

  beforeEach(() => {
    return MockBuilder(SkillstarAdminComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(SkillstarAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
