import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {AutocompleteSectionComponent} from './autocomplete-section.component';

describe('AutocompleteSectionComponent', () => {
  let component: AutocompleteSectionComponent;
  let fixture: MockedComponentFixture<AutocompleteSectionComponent>;

  beforeEach(() => {
    return MockBuilder(AutocompleteSectionComponent);
  });

  beforeEach(() => {
    fixture = MockRender(AutocompleteSectionComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
