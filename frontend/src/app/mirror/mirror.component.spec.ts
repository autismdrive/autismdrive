import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {MirrorComponent} from './mirror.component';

describe('MirrorComponent', () => {
  let component: MirrorComponent;
  let fixture: MockedComponentFixture<MirrorComponent>;

  beforeEach(() => {
    return MockBuilder(MirrorComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(MirrorComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
