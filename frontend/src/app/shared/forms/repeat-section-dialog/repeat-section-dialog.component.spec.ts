import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {customFormlyConfig} from '@app/app.config';
import {mockHousematesQuestionnaireMeta} from '@app/shared/fixtures/mock-housemates-questionnaire-meta';
import {keysToCamel} from '@app/shared/utilities/snakeToCamel';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {RepeatSectionDialogComponent} from './repeat-section-dialog.component';

describe('RepeatSectionDialogComponent', () => {
  let component: RepeatSectionDialogComponent;
  let fixture: MockedComponentFixture<RepeatSectionDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RepeatSectionDialogComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
      .mock(DeviceDetectorService)
      .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {
          title: 'Some title',
          fields: [keysToCamel(mockHousematesQuestionnaireMeta)],
          model: {},
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(RepeatSectionDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
