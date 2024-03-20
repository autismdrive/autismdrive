import {ComponentFixture, TestBed} from '@angular/core/testing';
import {GroupValidationWrapperComponent} from './group-validation-wrapper.component';

describe('GroupValidationWrapperComponent', () => {
  let component: GroupValidationWrapperComponent;
  let fixture: ComponentFixture<GroupValidationWrapperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GroupValidationWrapperComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupValidationWrapperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
