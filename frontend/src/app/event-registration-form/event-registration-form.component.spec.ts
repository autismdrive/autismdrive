import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {EventRegistrationFormComponent} from './event-registration-form.component';

describe('EventRegistrationFormComponent', () => {
  let component: EventRegistrationFormComponent;
  let fixture: ComponentFixture<EventRegistrationFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [EventRegistrationFormComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventRegistrationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
