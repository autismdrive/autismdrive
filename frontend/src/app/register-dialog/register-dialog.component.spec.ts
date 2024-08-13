import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {RegisterDialogComponent} from './register-dialog.component';

describe('RegisterDialogComponent', () => {
  let component: RegisterDialogComponent;
  let fixture: MockedComponentFixture<RegisterDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RegisterDialogComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(RegisterDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
