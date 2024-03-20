import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {AdminNoteFormComponent} from './admin-note-form.component';

describe('AdminNoteFormComponent', () => {
  let component: AdminNoteFormComponent;
  let fixture: ComponentFixture<AdminNoteFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AdminNoteFormComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminNoteFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
