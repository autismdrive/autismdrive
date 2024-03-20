import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {FlowCompleteComponent} from './flow-complete.component';

describe('FlowCompleteComponent', () => {
  let component: FlowCompleteComponent;
  let fixture: ComponentFixture<FlowCompleteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FlowCompleteComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlowCompleteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
