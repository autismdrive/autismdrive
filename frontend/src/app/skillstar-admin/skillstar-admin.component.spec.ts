import {ComponentFixture, TestBed} from '@angular/core/testing';
import {SkillstarAdminComponent} from './skillstar-admin.component';

describe('SkillstarAdminComponent', () => {
  let component: SkillstarAdminComponent;
  let fixture: ComponentFixture<SkillstarAdminComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SkillstarAdminComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SkillstarAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
