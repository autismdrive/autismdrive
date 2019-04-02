import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QuestionnaireDataTableComponent } from './questionnaire-data-table.component';

describe('QuestionnaireDataTableComponent', () => {
  let component: QuestionnaireDataTableComponent;
  let fixture: ComponentFixture<QuestionnaireDataTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ QuestionnaireDataTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuestionnaireDataTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
