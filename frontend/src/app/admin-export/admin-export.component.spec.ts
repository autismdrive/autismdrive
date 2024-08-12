import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {DataTransferLog} from '@models/data_transfer_log';
import {ApiService} from '@services/api/api.service';
import {ConfigService} from '@services/config/config.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {AdminExportComponent} from './admin-export.component';
import {of} from 'rxjs';

describe('AdminExportComponent', () => {
  let component: AdminExportComponent;
  let fixture: MockedComponentFixture<AdminExportComponent>;

  beforeEach(() => {
    return MockBuilder(AdminExportComponent, AppModule)
      .mock(ApiService, {
        getDataTransferLogs: jest.fn().mockReturnValue(
          of({
            pages: 0,
            total: 0,
            items: [],
          }),
        ),
      })
      .mock(ConfigService, {})
      .keep(MaterialModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(AdminExportComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
