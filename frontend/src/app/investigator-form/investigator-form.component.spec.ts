import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {mockStudyInvestigator} from '@util/testing/fixtures/mock-study-investigator';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {InvestigatorFormComponent} from './investigator-form.component';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

describe('InvestigatorFormComponent', () => {
  let component: InvestigatorFormComponent;
  let fixture: MockedComponentFixture<InvestigatorFormComponent>;

  beforeEach(() => {
    return MockBuilder(InvestigatorFormComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(MaterialModule)
      .keep(FormsModule)
      .keep(ReactiveFormsModule)
      .keep(MaterialModule)
      .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {
          si: mockStudyInvestigator,
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(InvestigatorFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
