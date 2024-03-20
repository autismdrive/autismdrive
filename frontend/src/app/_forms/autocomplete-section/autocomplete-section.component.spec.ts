import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {AutocompleteSectionComponent} from './autocomplete-section.component';

describe('AutocompleteSectionComponent', () => {
  let component: AutocompleteSectionComponent;
  let fixture: ComponentFixture<AutocompleteSectionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AutocompleteSectionComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AutocompleteSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
