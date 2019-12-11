import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParticipantAdminComponent } from './participant-admin.component';

describe('ParticipantAdminComponent', () => {
  let component: ParticipantAdminComponent;
  let fixture: ComponentFixture<ParticipantAdminComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParticipantAdminComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
