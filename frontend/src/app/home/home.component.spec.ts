import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {ConfigService} from '@services/config/config.service';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {HomeComponent} from './home.component';
import {RouterModule} from '@angular/router';
import {of} from 'rxjs';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: MockedComponentFixture<HomeComponent>;

  beforeEach(() => {
    return MockBuilder(HomeComponent, AppModule)
      .keep(RouterModule)
      .mock(ConfigService)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getStudiesByStatus: jest.fn().mockReturnValue(of([mockStudy])),
      });
  });

  beforeEach(() => {
    fixture = MockRender(HomeComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
