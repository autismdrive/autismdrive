import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ResourceAddButtonComponent } from './resource-add-button.component';

describe('ResourceAddButtonComponent', () => {
  let component: ResourceAddButtonComponent;
  let fixture: ComponentFixture<ResourceAddButtonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ResourceAddButtonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResourceAddButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
