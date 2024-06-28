import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {StudiesComponent} from './studies.component';

describe('StudiesComponent', () => {
  let component: StudiesComponent;
  let fixture: MockedComponentFixture<StudiesComponent>;

  beforeEach(() => {
    return MockBuilder(StudiesComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(StudiesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
