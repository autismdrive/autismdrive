import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FilterChipsComponent} from './filter-chips.component';
import {RouterModule} from '@angular/router';

describe('CategoryChipsComponent', () => {
  let component: FilterChipsComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FilterChipsComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(MaterialModule)
      .keep(RouterModule)
      .mock(GoogleAnalyticsService);
  });

  beforeEach(() => {
    fixture = MockRender(
      FilterChipsComponent,
      {
        categories: [],
        ages: [],
        languages: [],
        covid19_categories: [],
        parentComponent: 'resource-detail',
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
