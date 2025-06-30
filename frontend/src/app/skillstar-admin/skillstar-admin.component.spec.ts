import {mockChainStep} from '@app/shared/fixtures/mock-chain-step';
import {ApiService} from '@services/api/api.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {SkillstarAdminComponent} from './skillstar-admin.component';

describe('SkillstarAdminComponent', () => {
  let component: SkillstarAdminComponent;
  let fixture: MockedComponentFixture<SkillstarAdminComponent>;

  beforeEach(() => {
    return MockBuilder(SkillstarAdminComponent)
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
