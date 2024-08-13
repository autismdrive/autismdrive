import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ParticipantDetailComponent} from './participant-detail.component';

describe('ParticipantDetailComponent', () => {
  let component: ParticipantDetailComponent;
  let fixture: MockedComponentFixture<ParticipantDetailComponent>;

  beforeEach(() => {
    return MockBuilder(ParticipantDetailComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ParticipantDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
