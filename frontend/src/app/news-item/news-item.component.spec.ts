import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {NewsItemComponent} from './news-item.component';

describe('NewsItemComponent', () => {
  let component: NewsItemComponent;
  let fixture: MockedComponentFixture<NewsItemComponent>;

  beforeEach(() => {
    return MockBuilder(NewsItemComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(NewsItemComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
