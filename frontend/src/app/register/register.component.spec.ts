import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {RegisterComponent} from './register.component';

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: MockedComponentFixture<RegisterComponent>;

  beforeEach(() => {
    return MockBuilder(RegisterComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(RegisterComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
