import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Profile_metaComponent } from './profile_meta.component';

describe('MetaComponent', () => {
  let component: Profile_metaComponent;
  let fixture: ComponentFixture<Profile_metaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Profile_metaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(Profile_metaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
