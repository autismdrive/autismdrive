import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {RepeatSectionDialogComponent} from './repeat-section-dialog.component';

describe('RepeatSectionDialogComponent', () => {
  let component: RepeatSectionDialogComponent;
  let fixture: MockedComponentFixture<RepeatSectionDialogComponent>;

  beforeEach(() => {
    return MockBuilder(RepeatSectionDialogComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(RepeatSectionDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
