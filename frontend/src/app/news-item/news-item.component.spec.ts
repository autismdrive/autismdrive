import {AppModule} from '@app/app.module';
import {HitType} from '@models/hit_type';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {NewsItemComponent} from './news-item.component';

describe('NewsItemComponent', () => {
  let component: NewsItemComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(NewsItemComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(
      NewsItemComponent,
      {
        item: {
          title: 'string',
          description: 'string',
          url: 'string',
          img: 'string',
          type: HitType.RESOURCE,
        },
        index: 0,
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
