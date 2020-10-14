import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchFiltersBreadcrumbsComponent } from './search-filters-breadcrumbs.component';

describe('SearchFiltersBreadcrumbsComponent', () => {
  let component: SearchFiltersBreadcrumbsComponent;
  let fixture: ComponentFixture<SearchFiltersBreadcrumbsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchFiltersBreadcrumbsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchFiltersBreadcrumbsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
