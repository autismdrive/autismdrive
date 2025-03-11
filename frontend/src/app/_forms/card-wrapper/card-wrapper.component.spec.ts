import {By} from '@angular/platform-browser';
import {FormlyConfig} from '@app/app.config';
import {CardWrapperComponent} from '@forms/card-wrapper/card-wrapper.component';
import {FormlyModule} from '@ngx-formly/core';
import {MockFormlyFormComponent} from '@util/testing/fixtures/mock-form.component';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';

describe('CardWrapperComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<MockFormlyFormComponent>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(CardWrapperComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(MockFormlyFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(fixture.debugElement.query(By.css('app-card-wrapper'))).toBeTruthy();
  });
});
