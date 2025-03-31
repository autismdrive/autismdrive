import {signal} from '@angular/core';
import {ApiService} from '@services/api/api.service';
import {ConfigService} from '@services/config/config.service';
import {mockConfigServiceProps} from '@util/testing/fixtures/mock-config-service-props';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {AdminExportComponent} from './admin-export.component';

describe('AdminExportComponent', () => {
  let component: AdminExportComponent;
  let fixture: MockedComponentFixture<AdminExportComponent>;

  beforeEach(() => {
    return MockBuilder(AdminExportComponent)
      .mock(ApiService, {
        getDataTransferLogs: jest.fn().mockReturnValue(
          of({
            pages: 0,
            total: 0,
            items: [],
          }),
        ),
      })
      .mock(ConfigService, {props: signal(mockConfigServiceProps)})
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
