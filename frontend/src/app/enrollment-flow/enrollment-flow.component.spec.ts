import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EnrollmentFlowComponent } from './enrollment-flow.component';

describe('EnrollmentFlowComponent', () => {
  let component: EnrollmentFlowComponent;
  let fixture: ComponentFixture<EnrollmentFlowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EnrollmentFlowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EnrollmentFlowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
