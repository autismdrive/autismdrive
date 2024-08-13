import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {SearchTopicsComponent} from './search-topics.component';

describe('SearchTopicsComponent', () => {
  let component: SearchTopicsComponent;
  let fixture: MockedComponentFixture<SearchTopicsComponent>;

  beforeEach(() => {
    return MockBuilder(SearchTopicsComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(SearchTopicsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
