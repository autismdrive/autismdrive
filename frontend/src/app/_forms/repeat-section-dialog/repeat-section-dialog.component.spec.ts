import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {FormlyConfig} from '@app/app.config';
import {FormlyModule} from '@ngx-formly/core';
import {keysToCamel} from '@util/snakeToCamel';
import {mockHousematesQuestionnaireMeta} from '@util/testing/fixtures/mock-housemates-questionnaire-meta';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {RepeatSectionDialogComponent} from './repeat-section-dialog.component';

describe('RepeatSectionDialogComponent', () => {
  let component: RepeatSectionDialogComponent;
  let fixture: MockedComponentFixture<RepeatSectionDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RepeatSectionDialogComponent)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
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
