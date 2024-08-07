import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AddButtonComponent} from './add-button.component';

describe('AddButtonComponent', () => {
  let component: AddButtonComponent;
  let fixture: MockedComponentFixture<AddButtonComponent>;

  beforeEach(() => {
    return MockBuilder(AddButtonComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AddButtonComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
