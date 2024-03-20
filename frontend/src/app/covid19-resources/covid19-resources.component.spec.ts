import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {Covid19ResourcesComponent} from './covid19-resources.component';

describe('Covid19ResourcesComponent', () => {
  let component: Covid19ResourcesComponent;
  let fixture: ComponentFixture<Covid19ResourcesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [Covid19ResourcesComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Covid19ResourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
