import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {SearchTopicsComponent} from './search-topics.component';

describe('SearchTopicsComponent', () => {
  let component: SearchTopicsComponent;
  let fixture: MockedComponentFixture<SearchTopicsComponent>;

  beforeEach(() => {
    return MockBuilder(SearchTopicsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SearchTopicsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
