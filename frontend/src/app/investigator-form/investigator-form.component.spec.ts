import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {InvestigatorFormComponent} from './investigator-form.component';

describe('InvestigatorFormComponent', () => {
  let component: InvestigatorFormComponent;
  let fixture: MockedComponentFixture<InvestigatorFormComponent>;

  beforeEach(() => {
    return MockBuilder(InvestigatorFormComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(InvestigatorFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
