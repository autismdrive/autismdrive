import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {UvaEducationComponent} from './uva-education.component';

describe('UvaEducationComponent', () => {
  let component: UvaEducationComponent;
  let fixture: MockedComponentFixture<UvaEducationComponent>;

  beforeEach(() => {
    return MockBuilder(UvaEducationComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(UvaEducationComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
