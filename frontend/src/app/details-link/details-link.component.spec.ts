import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {DetailsLinkComponent} from './details-link.component';

describe('DetailsLinkComponent', () => {
  let component: DetailsLinkComponent;
  let fixture: MockedComponentFixture<DetailsLinkComponent>;

  beforeEach(() => {
    return MockBuilder(DetailsLinkComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(DetailsLinkComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
