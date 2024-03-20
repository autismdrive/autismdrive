import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {TimedoutComponent} from './timed-out.component';

describe('TimedoutComponent', () => {
  let component: TimedoutComponent;
  let fixture: ComponentFixture<TimedoutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TimedoutComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimedoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
