import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FavoriteResourceButtonComponent} from './favorite-resource-button.component';

describe('FavoriteButtonComponent', () => {
  let component: FavoriteResourceButtonComponent;
  let fixture: MockedComponentFixture<FavoriteResourceButtonComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteResourceButtonComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteResourceButtonComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
