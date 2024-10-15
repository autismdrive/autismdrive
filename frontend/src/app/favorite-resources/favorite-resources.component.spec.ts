import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FavoriteResourcesComponent} from './favorite-resources.component';

describe('FavoriteResourcesComponent', () => {
  let component: FavoriteResourcesComponent;
  let fixture: MockedComponentFixture<FavoriteResourcesComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteResourcesComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteResourcesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
