import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {CardWrapperComponent} from './card-wrapper.component';

describe('CardWrapperComponent', () => {
  let component: CardWrapperComponent;
  let fixture: MockedComponentFixture<CardWrapperComponent>;

  beforeEach(() => {
    return MockBuilder(CardWrapperComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(CardWrapperComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
