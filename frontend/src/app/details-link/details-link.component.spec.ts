import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DetailsLinkComponent} from './details-link.component';

describe('DetailsLinkComponent', () => {
  let component: DetailsLinkComponent;
  let fixture: MockedComponentFixture<DetailsLinkComponent>;

  beforeEach(() => {
    return MockBuilder(DetailsLinkComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(DetailsLinkComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
