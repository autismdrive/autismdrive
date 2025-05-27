import {signal} from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@app/shared/services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';
import {mockResourceDetailsRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {ResourceDetailComponent} from './resource-detail.component';

describe('ResourceDetailComponent', () => {
  let component: ResourceDetailComponent;
  let fixture: MockedComponentFixture<ResourceDetailComponent>;

  beforeEach(() => {
    return MockBuilder(ResourceDetailComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {getResourceChangeLog: jest.fn().mockReturnValue(of([]))})
      .provide({provide: ActivatedRoute, useValue: mockResourceDetailsRoute})
      .keep(RouterModule)
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(GoogleMapsLibraryService, {core: signal(undefined)})
      .mock(DomSanitizer);
  });

  beforeEach(() => {
    fixture = MockRender(ResourceDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
