import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxonomyAdminComponent } from './taxonomy-admin.component';

describe('TaxonomyAdminComponent', () => {
  let component: TaxonomyAdminComponent;
  let fixture: ComponentFixture<TaxonomyAdminComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxonomyAdminComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxonomyAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
