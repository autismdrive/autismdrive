import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FormPrintoutComponent} from './form-printout.component';

describe('FormPrintoutComponent', () => {
  let component: FormPrintoutComponent;
  let fixture: MockedComponentFixture<FormPrintoutComponent>;

  beforeEach(() => {
    return MockBuilder(FormPrintoutComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FormPrintoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
