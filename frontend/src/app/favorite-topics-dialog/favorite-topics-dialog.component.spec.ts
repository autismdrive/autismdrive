import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FavoriteTopicsDialogComponent} from './favorite-topics-dialog.component';

describe('FavoriteTopicsDialogComponent', () => {
  let component: FavoriteTopicsDialogComponent;
  let fixture: MockedComponentFixture<FavoriteTopicsDialogComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsDialogComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteTopicsDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
