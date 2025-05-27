import {customFormlyConfig} from '@app/app.config';
import {FormlyModule} from '@ngx-formly/core';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FormPrintoutComponent} from './form-printout.component';

describe('FormPrintoutComponent', () => {
  let component: FormPrintoutComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FormPrintoutComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(FormlyModule.forRoot(customFormlyConfig));
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
