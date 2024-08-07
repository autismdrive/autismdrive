import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FooterComponent} from './footer.component';

describe('FooterComponent', () => {
  let component: FooterComponent;
  let fixture: MockedComponentFixture<FooterComponent>;

  beforeEach(() => {
    return MockBuilder(FooterComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FooterComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
