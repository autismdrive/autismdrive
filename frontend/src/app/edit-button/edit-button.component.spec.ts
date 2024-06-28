import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {EditButtonComponent} from './edit-button.component';

describe('EditButtonComponent', () => {
  let component: EditButtonComponent;
  let fixture: MockedComponentFixture<EditButtonComponent>;

  beforeEach(() => {
    return MockBuilder(EditButtonComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(EditButtonComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
