import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {FiltersComponent} from './filters.component';

describe('FiltersComponent', () => {
  let component: FiltersComponent;
  let fixture: MockedComponentFixture<FiltersComponent>;

  beforeEach(() => {
    return MockBuilder(FiltersComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FiltersComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
