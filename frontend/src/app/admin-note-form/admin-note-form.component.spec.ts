import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AdminNoteFormComponent} from './admin-note-form.component';

describe('AdminNoteFormComponent', () => {
  let component: AdminNoteFormComponent;
  let fixture: MockedComponentFixture<AdminNoteFormComponent>;

  beforeEach(() => {
    return MockBuilder(AdminNoteFormComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AdminNoteFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
