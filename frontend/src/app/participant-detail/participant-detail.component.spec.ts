import {mockParticipant} from '@app/shared/fixtures/mock-participant';
import {ApiService} from '@services/api/api.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {ParticipantDetailComponent} from './participant-detail.component';

describe('ParticipantDetailComponent', () => {
  let component: ParticipantDetailComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(ParticipantDetailComponent)
      .mock(ApiService, {getParticipantStepLog: jest.fn().mockReturnValue(of([]))})
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantDetailComponent, {participant: mockParticipant}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
