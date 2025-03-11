import {By} from '@angular/platform-browser';
import {FormlyConfig} from '@app/app.config';
import {RepeatSectionComponent} from '@forms/repeat-section/repeat-section.component';
import {FormlyModule} from '@ngx-formly/core';
import {MockFormlyFormComponent} from '@util/testing/fixtures/mock-form.component';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';

describe('RepeatSectionComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<MockFormlyFormComponent>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(RepeatSectionComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(MockFormlyFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(fixture.debugElement.query(By.css('app-repeat-section'))).toBeTruthy();
    expect(fixture.debugElement.query(By.css('.repeat-action'))).toBeTruthy();
  });
});
