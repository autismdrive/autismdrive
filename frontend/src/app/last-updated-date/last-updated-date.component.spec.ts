import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {LastUpdatedDateComponent} from './last-updated-date.component';

describe('LastUpdatedDateComponent', () => {
  let component: LastUpdatedDateComponent;
  let fixture: MockedComponentFixture<LastUpdatedDateComponent>;

  beforeEach(() => {
    return MockBuilder(LastUpdatedDateComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(LastUpdatedDateComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
