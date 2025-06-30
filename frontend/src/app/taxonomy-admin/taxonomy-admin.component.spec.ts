import {signal} from '@angular/core';
import {mockCategory} from '@app/shared/fixtures/mock-category';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@app/shared/services/api/api.service';
import {AuthenticationService} from '@app/shared/services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {TaxonomyAdminComponent} from './taxonomy-admin.component';

describe('TaxonomyAdminComponent', () => {
  let component: TaxonomyAdminComponent;
  let fixture: MockedComponentFixture<TaxonomyAdminComponent>;

  beforeEach(() => {
    return MockBuilder(TaxonomyAdminComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getCategoryTree: jest.fn().mockReturnValue(of([mockCategory])),
        addCategory: jest.fn().mockReturnValue(of(mockCategory)),
        deleteCategory: jest.fn().mockReturnValue(of(mockCategory)),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)});
  });

  beforeEach(() => {
    fixture = MockRender(TaxonomyAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
