import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {HomeComponent} from './home.component';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: MockedComponentFixture<HomeComponent>;

  beforeEach(() => {
    return MockBuilder(HomeComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(HomeComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
