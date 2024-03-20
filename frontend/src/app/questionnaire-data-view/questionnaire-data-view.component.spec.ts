import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {QuestionnaireDataViewComponent} from './questionnaire-data-view.component';

describe('QuestionnaireDataViewComponent', () => {
  let component: QuestionnaireDataViewComponent;
  let fixture: ComponentFixture<QuestionnaireDataViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [QuestionnaireDataViewComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuestionnaireDataViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
