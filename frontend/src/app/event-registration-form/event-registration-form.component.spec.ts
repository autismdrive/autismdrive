import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {EventRegistrationFormComponent} from './event-registration-form.component';

describe('EventRegistrationFormComponent', () => {
  let component: EventRegistrationFormComponent;
  let fixture: MockedComponentFixture<EventRegistrationFormComponent>;

  beforeEach(() => {
    return MockBuilder(EventRegistrationFormComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(EventRegistrationFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
