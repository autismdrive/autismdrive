import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {AdminExportDetailsComponent} from './admin-export-details.component';

describe('AdminExportDetailsComponent', () => {
  let component: AdminExportDetailsComponent;
  let fixture: ComponentFixture<AdminExportDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AdminExportDetailsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminExportDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
