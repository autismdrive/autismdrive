import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {StudyInquiryComponent} from './study-inquiry.component';

describe('StudyInquiryComponent', () => {
  let component: StudyInquiryComponent;
  let fixture: MockedComponentFixture<StudyInquiryComponent>;

  beforeEach(() => {
    return MockBuilder(StudyInquiryComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(StudyInquiryComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
