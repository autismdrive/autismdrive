import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {RepeatSectionDialogComponent} from './repeat-section-dialog.component';

describe('RepeatSectionDialogComponent', () => {
  let component: RepeatSectionDialogComponent;
  let fixture: ComponentFixture<RepeatSectionDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [RepeatSectionDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RepeatSectionDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
