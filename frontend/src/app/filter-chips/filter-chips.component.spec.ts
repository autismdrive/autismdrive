import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FilterChipsComponent} from './filter-chips.component';

describe('CategoryChipsComponent', () => {
  let component: FilterChipsComponent;
  let fixture: MockedComponentFixture<FilterChipsComponent>;

  beforeEach(() => {
    return MockBuilder(FilterChipsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FilterChipsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
