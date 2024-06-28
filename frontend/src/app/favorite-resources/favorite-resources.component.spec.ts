import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {FavoriteResourcesComponent} from './favorite-resources.component';

describe('FavoriteResourcesComponent', () => {
  let component: FavoriteResourcesComponent;
  let fixture: MockedComponentFixture<FavoriteResourcesComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteResourcesComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteResourcesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
