import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {RegisterDialogComponent} from './register-dialog.component';

describe('RegisterDialogComponent', () => {
  let component: RegisterDialogComponent;
  let fixture: MockedComponentFixture<RegisterDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RegisterDialogComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(RegisterDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
