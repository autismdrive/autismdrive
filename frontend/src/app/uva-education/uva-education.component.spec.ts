import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UvaEducationComponent } from './uva-education.component';

describe('UvaEducationComponent', () => {
  let component: UvaEducationComponent;
  let fixture: ComponentFixture<UvaEducationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UvaEducationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UvaEducationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
