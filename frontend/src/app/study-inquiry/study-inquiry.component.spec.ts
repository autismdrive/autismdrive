import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyInquiryComponent } from './study-inquiry.component';

describe('StudyInquiryComponent', () => {
  let component: StudyInquiryComponent;
  let fixture: ComponentFixture<StudyInquiryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StudyInquiryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyInquiryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
