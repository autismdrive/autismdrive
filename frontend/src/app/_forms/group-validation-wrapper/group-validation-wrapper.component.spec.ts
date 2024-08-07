import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {GroupValidationWrapperComponent} from './group-validation-wrapper.component';

describe('GroupValidationWrapperComponent', () => {
  let component: GroupValidationWrapperComponent;
  let fixture: MockedComponentFixture<GroupValidationWrapperComponent>;

  beforeEach(() => {
    return MockBuilder(GroupValidationWrapperComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(GroupValidationWrapperComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
