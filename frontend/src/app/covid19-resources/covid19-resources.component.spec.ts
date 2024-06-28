import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {Covid19ResourcesComponent} from './covid19-resources.component';

describe('Covid19ResourcesComponent', () => {
  let component: Covid19ResourcesComponent;
  let fixture: MockedComponentFixture<Covid19ResourcesComponent>;

  beforeEach(() => {
    return MockBuilder(Covid19ResourcesComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(Covid19ResourcesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
