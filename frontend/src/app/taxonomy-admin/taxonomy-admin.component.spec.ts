import {AppModule} from '@app/app.module';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {TaxonomyAdminComponent} from './taxonomy-admin.component';
import {AuthenticationService} from '@app/_services/authentication/authentication-service';
import {ApiService} from '@app/_services/api/api.service';
import {of} from 'rxjs';

describe('TaxonomyAdminComponent', () => {
  let component: TaxonomyAdminComponent;
  let fixture: MockedComponentFixture<TaxonomyAdminComponent>;

  beforeEach(() => {
    return MockBuilder(TaxonomyAdminComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getCategoryTree: jest.fn().mockReturnValue(of([mockCategory])),
        addCategory: jest.fn().mockReturnValue(of(mockCategory)),
        deleteCategory: jest.fn().mockReturnValue(of(mockCategory)),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)});
  });

  beforeEach(() => {
    fixture = MockRender(TaxonomyAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
