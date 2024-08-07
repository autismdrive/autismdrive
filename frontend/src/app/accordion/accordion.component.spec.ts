import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AccordionComponent} from './accordion.component';

describe('AccordionComponent', () => {
  let component: AccordionComponent;
  let fixture: MockedComponentFixture<AccordionComponent>;

  beforeEach(() => {
    return MockBuilder(AccordionComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AccordionComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
