import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {ResourceFormComponent} from './resource-form.component';

describe('ResourceFormComponent', () => {
  let component: ResourceFormComponent;
  let fixture: MockedComponentFixture<ResourceFormComponent>;

  beforeEach(() => {
    return MockBuilder(ResourceFormComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ResourceFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
