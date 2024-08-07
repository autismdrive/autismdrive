import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {ParticipantProfileComponent} from './participant-profile.component';

describe('ParticipantProfileComponent', () => {
  let component: ParticipantProfileComponent;
  let fixture: MockedComponentFixture<ParticipantProfileComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantProfileComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantProfileComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
