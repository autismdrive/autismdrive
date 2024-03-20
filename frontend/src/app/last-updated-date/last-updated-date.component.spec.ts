import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {LastUpdatedDateComponent} from './last-updated-date.component';

describe('LastUpdatedDateComponent', () => {
  let component: LastUpdatedDateComponent;
  let fixture: ComponentFixture<LastUpdatedDateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [LastUpdatedDateComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LastUpdatedDateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
