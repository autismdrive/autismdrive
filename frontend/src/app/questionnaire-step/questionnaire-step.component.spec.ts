import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QuestionnaireStepComponent } from './questionnaire-step.component';

describe('QuestionnaireStepComponent', () => {
  let component: QuestionnaireStepComponent;
  let fixture: ComponentFixture<QuestionnaireStepComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ QuestionnaireStepComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuestionnaireStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
