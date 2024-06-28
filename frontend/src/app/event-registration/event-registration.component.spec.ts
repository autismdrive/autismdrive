import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {EventRegistrationComponent} from './event-registration.component';

describe('EventRegistrationComponent', () => {
  let component: EventRegistrationComponent;
  let fixture: MockedComponentFixture<EventRegistrationComponent>;

  beforeEach(() => {
    return MockBuilder(EventRegistrationComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(EventRegistrationComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
