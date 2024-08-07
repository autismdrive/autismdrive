import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {MultiselectTreeComponent} from './multiselect-tree.component';

describe('MultiselectTreeComponent', () => {
  let component: MultiselectTreeComponent;
  let fixture: MockedComponentFixture<MultiselectTreeComponent>;

  beforeEach(() => {
    return MockBuilder(MultiselectTreeComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(MultiselectTreeComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
