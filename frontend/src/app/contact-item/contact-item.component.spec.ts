import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {ContactItemComponent} from './contact-item.component';

describe('ContactItemComponent', () => {
  let component: ContactItemComponent;
  let fixture: MockedComponentFixture<ContactItemComponent>;

  beforeEach(() => {
    return MockBuilder(ContactItemComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ContactItemComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
