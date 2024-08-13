import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {AddButtonComponent} from './add-button.component';

describe('AddButtonComponent', () => {
  let component: AddButtonComponent;
  let fixture: MockedComponentFixture<AddButtonComponent>;

  beforeEach(() => {
    return MockBuilder(AddButtonComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(AddButtonComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
