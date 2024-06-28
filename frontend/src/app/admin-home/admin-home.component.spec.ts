import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {AdminHomeComponent} from './admin-home.component';

describe('AdminHomeComponent', () => {
  let component: AdminHomeComponent;
  let fixture: MockedComponentFixture<AdminHomeComponent>;

  beforeEach(() => {
    return MockBuilder(AdminHomeComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AdminHomeComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
