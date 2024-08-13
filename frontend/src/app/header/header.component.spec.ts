import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {HeaderComponent} from './header.component';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: MockedComponentFixture<HeaderComponent>;

  beforeEach(() => {
    return MockBuilder(HeaderComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(HeaderComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
