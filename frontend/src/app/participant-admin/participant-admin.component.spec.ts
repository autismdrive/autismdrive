import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ParticipantAdminComponent} from './participant-admin.component';

describe('ParticipantAdminComponent', () => {
  let component: ParticipantAdminComponent;
  let fixture: MockedComponentFixture<ParticipantAdminComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantAdminComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
