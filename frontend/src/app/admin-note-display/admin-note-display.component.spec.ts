import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {makeMockAdminNote} from '@util/testing/fixtures/mock-admin-note';
import {mockResource} from '@util/testing/fixtures/mock-resource';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {AdminNoteDisplayComponent} from './admin-note-display.component';

describe('AdminNoteDisplayComponent', () => {
  let component: AdminNoteDisplayComponent;
  let fixture: MockedComponentFixture<any>;
  const mockAdminNote = makeMockAdminNote({
    resource: mockResource,
    resource_id: mockResource.id,
    user: mockUser,
    user_id: mockUser.id,
  });

  beforeEach(() => {
    return MockBuilder(AdminNoteDisplayComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getResourceAdminNotes: jest.fn().mockReturnValue(of([mockAdminNote])),
        updateAdminNote: jest.fn().mockReturnValue(of(mockAdminNote)),
        deleteAdminNote: jest.fn().mockReturnValue(of(mockAdminNote)),
      });
  });

  beforeEach(() => {
    fixture = MockRender(
      AdminNoteDisplayComponent,
      {
        currentUser: mockUser,
        currentResource: mockResource,
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
