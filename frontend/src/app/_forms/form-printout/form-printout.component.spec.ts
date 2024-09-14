import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FormPrintoutComponent} from './form-printout.component';
import {FormlyModule} from '@ngx-formly/core';

describe('FormPrintoutComponent', () => {
  let component: FormPrintoutComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FormPrintoutComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS).keep(FormlyModule);
  });

  beforeEach(() => {
    fixture = MockRender(
      FormPrintoutComponent,
      {field: {model: {}, fieldGroup: [{fieldGroup: []}]}},
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
