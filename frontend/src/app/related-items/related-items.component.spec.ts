import {RouterModule} from '@angular/router';
import {mockResource} from '@app/shared/fixtures/mock-resource';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {RelatedItemsComponent} from './related-items.component';

describe('RelatedItemsComponent', () => {
  let component: RelatedItemsComponent;
  let fixture: MockedComponentFixture<RelatedItemsComponent>;

  beforeEach(() => {
    return MockBuilder(RelatedItemsComponent)
      .keep(RouterModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getRelatedResults: jest.fn().mockReturnValue(
          of([
            {
              resources: [mockResource],
              studies: [mockStudy],
            },
          ]),
        ),
      })
      .mock(GoogleAnalyticsService, {});
  });

  beforeEach(() => {
    fixture = MockRender(RelatedItemsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
