import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {ApiService} from '@services/api/api.service';
import {mockParticipantAdminList} from '@util/testing/fixtures/mock-participant-admin-list';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ParticipantAdminComponent} from './participant-admin.component';
import {of} from 'rxjs';

describe('ParticipantAdminComponent', () => {
  let component: ParticipantAdminComponent;
  let fixture: MockedComponentFixture<ParticipantAdminComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantAdminComponent, AppModule)
      .keep(MaterialModule)
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
