import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FormPrintoutComponent} from './form-printout.component';

describe('FormPrintoutComponent', () => {
  let component: FormPrintoutComponent;
  let fixture: MockedComponentFixture<FormPrintoutComponent>;

  beforeEach(() => {
    return MockBuilder(FormPrintoutComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FormPrintoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
