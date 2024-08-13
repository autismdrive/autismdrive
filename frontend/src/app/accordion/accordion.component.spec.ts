import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {AccordionComponent} from './accordion.component';

describe('AccordionComponent', () => {
  let component: AccordionComponent;
  let fixture: MockedComponentFixture<AccordionComponent>;

  beforeEach(() => {
    return MockBuilder(AccordionComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(AccordionComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
