import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {LoadingComponent} from './loading.component';

describe('LoadingComponent', () => {
  let component: LoadingComponent;
  let fixture: MockedComponentFixture<LoadingComponent>;

  beforeEach(() => {
    return MockBuilder(LoadingComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(LoadingComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
