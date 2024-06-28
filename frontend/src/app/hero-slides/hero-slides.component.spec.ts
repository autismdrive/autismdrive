import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {HeroSlidesComponent} from './hero-slides.component';

describe('HeroSlidesComponent', () => {
  let component: HeroSlidesComponent;
  let fixture: MockedComponentFixture<HeroSlidesComponent>;

  beforeEach(() => {
    return MockBuilder(HeroSlidesComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(HeroSlidesComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
