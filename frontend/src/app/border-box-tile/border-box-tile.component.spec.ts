import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {BorderBoxTileComponent} from './border-box-tile.component';

describe('BorderBoxTileComponent', () => {
  let component: BorderBoxTileComponent;
  let fixture: MockedComponentFixture<BorderBoxTileComponent>;

  beforeEach(() => {
    return MockBuilder(BorderBoxTileComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(BorderBoxTileComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
