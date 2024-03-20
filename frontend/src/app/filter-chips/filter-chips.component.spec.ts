import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {FilterChipsComponent} from './filter-chips.component';

describe('CategoryChipsComponent', () => {
  let component: FilterChipsComponent;
  let fixture: ComponentFixture<FilterChipsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FilterChipsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FilterChipsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
