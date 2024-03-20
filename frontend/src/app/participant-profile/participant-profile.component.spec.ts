import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {ParticipantProfileComponent} from './participant-profile.component';

describe('ParticipantProfileComponent', () => {
  let component: ParticipantProfileComponent;
  let fixture: ComponentFixture<ParticipantProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ParticipantProfileComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
