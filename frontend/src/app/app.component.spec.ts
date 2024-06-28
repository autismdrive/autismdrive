import {TestBed} from '@angular/core/testing';
import {RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {AppComponent} from './app.component';

describe('AppComponent', () => {
  let fixture: MockedComponentFixture<AppComponent>;
  let component: AppComponent;

  beforeEach(() => {
    return MockBuilder(AppComponent, AppModule).keep(RouterModule);
  });

  beforeEach(() => {
    fixture = MockRender(AppComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Autism DRIVE'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('Autism DRIVE');
  });

  it('should render title in a h1 tag', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('h1').textContent).toContain('Welcome to Autism DRIVE!');
  });
});
