import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {mockChainStep} from '@util/testing/fixtures/mockChainStep';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {SkillstarAdminComponent} from './skillstar-admin.component';
import {of} from 'rxjs';

describe('SkillstarAdminComponent', () => {
  let component: SkillstarAdminComponent;
  let fixture: MockedComponentFixture<SkillstarAdminComponent>;

  beforeEach(() => {
    return MockBuilder(SkillstarAdminComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getChainStepsList: jest.fn().mockReturnValue(of([mockChainStep])),
        deleteChainStep: jest.fn().mockReturnValue(of(mockChainStep)),
        editChainStep: jest.fn().mockReturnValue(of(mockChainStep)),
      });
  });

  beforeEach(() => {
    fixture = MockRender(SkillstarAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
