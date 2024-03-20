import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {StudyDetailComponent} from './study-detail.component';

describe('StudyDetailComponent', () => {
  let component: StudyDetailComponent;
  let fixture: ComponentFixture<StudyDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [StudyDetailComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
