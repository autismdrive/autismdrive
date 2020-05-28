import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteTopicsComponent } from './favorite-topics.component';

describe('FavoriteTopicsComponent', () => {
  let component: FavoriteTopicsComponent;
  let fixture: ComponentFixture<FavoriteTopicsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteTopicsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteTopicsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
