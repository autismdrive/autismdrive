import {ApiService} from '@services/api/api.service';
import {mockParticipantAdminList} from '@app/shared/fixtures/mock-participant-admin-list';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ParticipantAdminComponent} from './participant-admin.component';
import {of} from 'rxjs';

describe('ParticipantAdminComponent', () => {
  let component: ParticipantAdminComponent;
  let fixture: MockedComponentFixture<ParticipantAdminComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantAdminComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {getParticipantAdminList: jest.fn().mockReturnValue(of(mockParticipantAdminList))});
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
