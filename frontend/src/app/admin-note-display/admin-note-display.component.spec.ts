import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AdminNoteDisplayComponent} from './admin-note-display.component';

describe('AdminNoteDisplayComponent', () => {
  let component: AdminNoteDisplayComponent;
  let fixture: MockedComponentFixture<AdminNoteDisplayComponent>;

  beforeEach(() => {
    return MockBuilder(AdminNoteDisplayComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AdminNoteDisplayComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
