import {ComponentFixture, TestBed} from '@angular/core/testing';
import {ResizeTextareaComponent} from './resize-textarea.component';

describe('ResizeTextareaComponent', () => {
  let component: ResizeTextareaComponent;
  let fixture: ComponentFixture<ResizeTextareaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ResizeTextareaComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ResizeTextareaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
