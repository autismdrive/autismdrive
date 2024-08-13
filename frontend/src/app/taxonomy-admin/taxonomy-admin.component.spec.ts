import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {TaxonomyAdminComponent} from './taxonomy-admin.component';

describe('TaxonomyAdminComponent', () => {
  let component: TaxonomyAdminComponent;
  let fixture: MockedComponentFixture<TaxonomyAdminComponent>;

  beforeEach(() => {
    return MockBuilder(TaxonomyAdminComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(TaxonomyAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
