import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileMetaComponent } from './profile_meta.component';

describe('MetaComponent', () => {
  let component: ProfileMetaComponent;
  let fixture: ComponentFixture<ProfileMetaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileMetaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileMetaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
