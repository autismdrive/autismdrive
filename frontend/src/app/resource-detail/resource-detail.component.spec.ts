import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {ResourceDetailComponent} from './resource-detail.component';

describe('ResourceDetailComponent', () => {
  let component: ResourceDetailComponent;
  let fixture: MockedComponentFixture<ResourceDetailComponent>;

  beforeEach(() => {
    return MockBuilder(ResourceDetailComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ResourceDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
