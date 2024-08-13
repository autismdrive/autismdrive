import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {MultiselectTreeComponent} from './multiselect-tree.component';

describe('MultiselectTreeComponent', () => {
  let component: MultiselectTreeComponent;
  let fixture: MockedComponentFixture<MultiselectTreeComponent>;

  beforeEach(() => {
    return MockBuilder(MultiselectTreeComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(MultiselectTreeComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
