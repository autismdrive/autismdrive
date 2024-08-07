import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {TypeIconComponent} from './type-icon.component';

describe('TypeIconComponent', () => {
  let component: TypeIconComponent;
  let fixture: MockedComponentFixture<TypeIconComponent>;

  beforeEach(() => {
    return MockBuilder(TypeIconComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(TypeIconComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
