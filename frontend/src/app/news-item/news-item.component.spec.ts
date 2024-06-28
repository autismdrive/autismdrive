import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {NewsItemComponent} from './news-item.component';

describe('NewsItemComponent', () => {
  let component: NewsItemComponent;
  let fixture: MockedComponentFixture<NewsItemComponent>;

  beforeEach(() => {
    return MockBuilder(NewsItemComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(NewsItemComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
