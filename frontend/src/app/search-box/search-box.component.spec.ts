import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {SearchBoxComponent} from './search-box.component';

describe('SearchBoxComponent', () => {
  let component: SearchBoxComponent;
  let fixture: MockedComponentFixture<SearchBoxComponent>;

  beforeEach(() => {
    return MockBuilder(SearchBoxComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SearchBoxComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
