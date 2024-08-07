import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AboutComponent} from './about.component';

describe('AboutComponent', () => {
  let component: AboutComponent;
  let fixture: MockedComponentFixture<AboutComponent>;

  beforeEach(() => {
    return MockBuilder(AboutComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(AboutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
