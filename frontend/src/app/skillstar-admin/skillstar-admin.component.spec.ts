import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {SkillstarAdminComponent} from './skillstar-admin.component';

describe('SkillstarAdminComponent', () => {
  let component: SkillstarAdminComponent;
  let fixture: MockedComponentFixture<SkillstarAdminComponent>;

  beforeEach(() => {
    return MockBuilder(SkillstarAdminComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SkillstarAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
