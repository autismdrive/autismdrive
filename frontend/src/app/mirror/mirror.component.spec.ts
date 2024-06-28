import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {MirrorComponent} from './mirror.component';

describe('MirrorComponent', () => {
  let component: MirrorComponent;
  let fixture: MockedComponentFixture<MirrorComponent>;

  beforeEach(() => {
    return MockBuilder(MirrorComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(MirrorComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
