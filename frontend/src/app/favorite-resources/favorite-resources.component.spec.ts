import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteResourcesComponent } from './favorite-resources.component';

describe('FavoriteResourcesComponent', () => {
  let component: FavoriteResourcesComponent;
  let fixture: ComponentFixture<FavoriteResourcesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteResourcesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteResourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
