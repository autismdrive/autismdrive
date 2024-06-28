import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {RepeatSectionComponent} from './repeat-section.component';

describe('RepeatSectionComponent', () => {
  let component: RepeatSectionComponent;
  let fixture: MockedComponentFixture<RepeatSectionComponent>;

  beforeEach(() => {
    return MockBuilder(RepeatSectionComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(RepeatSectionComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
