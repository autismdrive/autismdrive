import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ResourceEditButtonComponent } from './resource-edit-button.component';

describe('ResourceEditButtonComponent', () => {
  let component: ResourceEditButtonComponent;
  let fixture: ComponentFixture<ResourceEditButtonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ResourceEditButtonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResourceEditButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
