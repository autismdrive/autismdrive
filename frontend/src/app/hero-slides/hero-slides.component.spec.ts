import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {HeroSlidesComponent} from './hero-slides.component';

describe('HeroSlidesComponent', () => {
  let component: HeroSlidesComponent;
  let fixture: MockedComponentFixture<HeroSlidesComponent>;

  beforeEach(() => {
    return MockBuilder(HeroSlidesComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(HeroSlidesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
