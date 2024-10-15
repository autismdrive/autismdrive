import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {mockAdminNote} from '@util/testing/fixtures/mock-admin-note';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {RepeatSectionDialogComponent} from './repeat-section-dialog.component';
import {DeviceDetectorService} from 'ngx-device-detector';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

describe('RepeatSectionDialogComponent', () => {
  let component: RepeatSectionDialogComponent;
  let fixture: MockedComponentFixture<RepeatSectionDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RepeatSectionDialogComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(DeviceDetectorService)
      .keep(MaterialModule)
      .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {
          title: 'Some title',
          fields: [],
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
