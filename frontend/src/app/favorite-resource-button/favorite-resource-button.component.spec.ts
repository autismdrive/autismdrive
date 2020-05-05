import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteResourceButtonComponent } from './favorite-resource-button.component';

describe('FavoriteButtonComponent', () => {
  let component: FavoriteResourceButtonComponent;
  let fixture: ComponentFixture<FavoriteResourceButtonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteResourceButtonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteResourceButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
