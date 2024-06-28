import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {ParticipantAdminComponent} from './participant-admin.component';

describe('ParticipantAdminComponent', () => {
  let component: ParticipantAdminComponent;
  let fixture: MockedComponentFixture<ParticipantAdminComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantAdminComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
