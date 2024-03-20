import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {InvestigatorFormComponent} from './investigator-form.component';

describe('InvestigatorFormComponent', () => {
  let component: InvestigatorFormComponent;
  let fixture: ComponentFixture<InvestigatorFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [InvestigatorFormComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InvestigatorFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
