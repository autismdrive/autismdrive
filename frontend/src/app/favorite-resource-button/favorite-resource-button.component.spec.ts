import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FavoriteResourceButtonComponent} from './favorite-resource-button.component';

describe('FavoriteButtonComponent', () => {
  let component: FavoriteResourceButtonComponent;
  let fixture: MockedComponentFixture<FavoriteResourceButtonComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteResourceButtonComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteResourceButtonComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
