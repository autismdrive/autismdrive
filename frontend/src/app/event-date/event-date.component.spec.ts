import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {EventDateComponent} from './event-date.component';

describe('EventDateComponent', () => {
  let component: EventDateComponent;
  let fixture: MockedComponentFixture<EventDateComponent>;

  beforeEach(() => {
    return MockBuilder(EventDateComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(EventDateComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
