import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminExportComponent } from './admin-export.component';

describe('AdminExportComponent', () => {
  let component: AdminExportComponent;
  let fixture: ComponentFixture<AdminExportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdminExportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminExportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
