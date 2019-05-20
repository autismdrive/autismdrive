import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HeroSlidesComponent } from './hero-slides.component';

describe('HeroSlidesComponent', () => {
  let component: HeroSlidesComponent;
  let fixture: ComponentFixture<HeroSlidesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HeroSlidesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HeroSlidesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
