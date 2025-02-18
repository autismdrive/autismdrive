import {TestBed} from '@angular/core/testing';
import {RouterModule} from '@angular/router';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AppComponent} from './app.component';

describe('AppComponent', () => {
  let fixture: MockedComponentFixture<AppComponent>;
  let component: AppComponent;

  beforeEach(() => {
    return MockBuilder(AppComponent).keep(RouterModule).keep(AuthenticationService);
  });

  beforeEach(() => {
    fixture = MockRender(AppComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Autism DRIVE'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('Autism DRIVE');
  });
});
