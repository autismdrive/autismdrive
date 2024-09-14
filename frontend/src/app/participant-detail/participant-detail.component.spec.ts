import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {ApiService} from '@services/api/api.service';
import {mockParticipant} from '@util/testing/fixtures/mock-participant';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ParticipantDetailComponent} from './participant-detail.component';
import {of} from 'rxjs';

describe('ParticipantDetailComponent', () => {
  let component: ParticipantDetailComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(ParticipantDetailComponent, AppModule)
      .keep(MaterialModule)
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
