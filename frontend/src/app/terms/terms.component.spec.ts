import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {TermsComponent} from './terms.component';

describe('TermsComponent', () => {
  let component: TermsComponent;
  let fixture: MockedComponentFixture<TermsComponent>;

  beforeEach(() => {
    return MockBuilder(TermsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(TermsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
