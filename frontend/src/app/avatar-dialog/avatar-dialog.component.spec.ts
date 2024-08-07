import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AvatarDialogComponent} from './avatar-dialog.component';

describe('AvatarDialogComponent', () => {
  let component: AvatarDialogComponent;
  let fixture: MockedComponentFixture<AvatarDialogComponent>;

  beforeEach(() => {
    return MockBuilder(AvatarDialogComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AvatarDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
