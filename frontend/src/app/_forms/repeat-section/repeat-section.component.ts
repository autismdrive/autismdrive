import {CommonModule} from '@angular/common';
import {Component} from '@angular/core';
import {MatButtonModule, MatIconButton} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatDialog} from '@angular/material/dialog';
import {MatIconModule} from '@angular/material/icon';
import {FormPrintoutComponent} from '@forms/form-printout/form-printout.component';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FieldArrayType, FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {RepeatSectionDialogComponent} from '../repeat-section-dialog/repeat-section-dialog.component';

@Component({
  standalone: true,
  selector: 'app-repeat-section',
  templateUrl: './repeat-section.component.html',
  styleUrls: ['./repeat-section.component.scss'],
  imports: [
    CommonModule,
    FlexModule,
    FormPrintoutComponent,
    FormlyModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
  ],
})
export class RepeatSectionComponent extends FieldArrayType {
  constructor(public dialog: MatDialog) {
    super();
  }

  openDialog(i: number, f?: FormlyFieldConfig) {
    const isEdit = !!f;
    const title = this.field.props.description;
    const dialogRef = this.dialog.open(RepeatSectionDialogComponent, {
      maxWidth: '100vw',
      maxHeight: '100vh',
      minWidth: '70vw',
      data: {
        title: isEdit ? title.replace(/^Add an|^Add a|^Add/, 'Edit') : title,
        fields: [this.field.fieldArray],
        model: isEdit ? this.field.fieldGroup[i].model : {},
      },
    });

    dialogRef.afterClosed().subscribe(data => {
      if (data && data.model) {
        if (this.field.fieldGroup.length > i) {
          super.remove(i);
        }

        super.add(i, data.model);
      }
    });
  }
}
