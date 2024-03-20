import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {FormPrintoutComponent} from './form-printout.component';

describe('FormPrintoutComponent', () => {
  let component: FormPrintoutComponent;
  let fixture: ComponentFixture<FormPrintoutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FormPrintoutComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FormPrintoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
