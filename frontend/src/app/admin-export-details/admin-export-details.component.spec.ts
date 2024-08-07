import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AdminExportDetailsComponent} from './admin-export-details.component';

describe('AdminExportDetailsComponent', () => {
  let component: AdminExportDetailsComponent;
  let fixture: MockedComponentFixture<AdminExportDetailsComponent>;

  beforeEach(() => {
    return MockBuilder(AdminExportDetailsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AdminExportDetailsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
