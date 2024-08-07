import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FavoriteTopicsComponent} from './favorite-topics.component';

describe('FavoriteTopicsComponent', () => {
  let component: FavoriteTopicsComponent;
  let fixture: MockedComponentFixture<FavoriteTopicsComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteTopicsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
