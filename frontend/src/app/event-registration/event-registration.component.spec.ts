import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventRegistrationComponent } from './event-registration.component';

describe('EventRegistrationComponent', () => {
  let component: EventRegistrationComponent;
  let fixture: ComponentFixture<EventRegistrationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventRegistrationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventRegistrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
