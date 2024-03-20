import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {FavoriteTopicsDialogComponent} from './favorite-topics-dialog.component';

describe('FavoriteTopicsDialogComponent', () => {
  let component: FavoriteTopicsDialogComponent;
  let fixture: ComponentFixture<FavoriteTopicsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FavoriteTopicsDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteTopicsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
