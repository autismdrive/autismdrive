import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {EmailLogAdminComponent} from './email-log-admin.component';

describe('EmailLogAdminComponent', () => {
  let component: EmailLogAdminComponent;
  let fixture: ComponentFixture<EmailLogAdminComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [EmailLogAdminComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EmailLogAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
