import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {RelatedItemsComponent} from './related-items.component';

describe('RelatedItemsComponent', () => {
  let component: RelatedItemsComponent;
  let fixture: MockedComponentFixture<RelatedItemsComponent>;

  beforeEach(() => {
    return MockBuilder(RelatedItemsComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(RelatedItemsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
