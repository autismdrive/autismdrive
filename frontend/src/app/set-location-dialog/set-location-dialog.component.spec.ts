import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SetLocationDialogComponent } from './set-location-dialog.component';

describe('SetLocationDialogComponent', () => {
  let component: SetLocationDialogComponent;
  let fixture: ComponentFixture<SetLocationDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SetLocationDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SetLocationDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
