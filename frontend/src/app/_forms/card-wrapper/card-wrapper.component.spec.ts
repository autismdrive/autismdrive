import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {CardWrapperComponent} from './card-wrapper.component';

describe('CardWrapperComponent', () => {
  let component: CardWrapperComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(CardWrapperComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(CardWrapperComponent, {props: {}}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
