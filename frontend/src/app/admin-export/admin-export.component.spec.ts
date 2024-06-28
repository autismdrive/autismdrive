import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {AdminExportComponent} from './admin-export.component';

describe('AdminExportComponent', () => {
  let component: AdminExportComponent;
  let fixture: MockedComponentFixture<AdminExportComponent>;

  beforeEach(() => {
    return MockBuilder(AdminExportComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AdminExportComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
