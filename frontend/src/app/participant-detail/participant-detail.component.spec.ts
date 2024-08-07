import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {ParticipantDetailComponent} from './participant-detail.component';

describe('ParticipantDetailComponent', () => {
  let component: ParticipantDetailComponent;
  let fixture: MockedComponentFixture<ParticipantDetailComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantDetailComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
