import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {FlowIntroComponent} from './flow-intro.component';

describe('FlowIntroComponent', () => {
  let component: FlowIntroComponent;
  let fixture: ComponentFixture<FlowIntroComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FlowIntroComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlowIntroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
