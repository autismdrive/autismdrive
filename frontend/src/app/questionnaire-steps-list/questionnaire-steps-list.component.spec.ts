import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {QuestionnaireStepsListComponent} from './questionnaire-steps-list.component';

describe('QuestionnaireStepsListComponent', () => {
  let component: QuestionnaireStepsListComponent;
  let fixture: ComponentFixture<QuestionnaireStepsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [QuestionnaireStepsListComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuestionnaireStepsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
