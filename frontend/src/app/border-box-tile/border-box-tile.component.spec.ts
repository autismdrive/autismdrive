import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BorderBoxTileComponent } from './border-box-tile.component';

describe('BorderBoxTileComponent', () => {
  let component: BorderBoxTileComponent;
  let fixture: ComponentFixture<BorderBoxTileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BorderBoxTileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BorderBoxTileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
