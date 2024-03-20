import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {AdminNoteDisplayComponent} from './admin-note-display.component';

describe('AdminNoteDisplayComponent', () => {
  let component: AdminNoteDisplayComponent;
  let fixture: ComponentFixture<AdminNoteDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AdminNoteDisplayComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminNoteDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
