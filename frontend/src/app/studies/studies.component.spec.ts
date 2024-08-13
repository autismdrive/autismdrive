import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {StudiesComponent} from './studies.component';

describe('StudiesComponent', () => {
  let component: StudiesComponent;
  let fixture: MockedComponentFixture<StudiesComponent>;

  beforeEach(() => {
    return MockBuilder(StudiesComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(StudiesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
