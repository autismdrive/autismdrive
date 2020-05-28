import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudySurveyEntryComponent } from './study-survey-entry.component';

describe('StudySurveyEntryComponent', () => {
  let component: StudySurveyEntryComponent;
  let fixture: ComponentFixture<StudySurveyEntryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StudySurveyEntryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudySurveyEntryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
