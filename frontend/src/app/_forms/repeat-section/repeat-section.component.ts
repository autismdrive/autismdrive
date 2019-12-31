import {Component} from '@angular/core';
import {FieldArrayType, FormlyFieldConfig} from '@ngx-formly/core';
import {MatDialog} from '@angular/material/dialog';
import {RepeatSectionDialogComponent} from '../repeat-section-dialog/repeat-section-dialog.component';

@Component({
  selector: 'app-repeat-section',
  templateUrl: './repeat-section.component.html',
  styleUrls: ['./repeat-section.component.scss']
})
export class RepeatSectionComponent extends FieldArrayType {
  constructor(
    public dialog: MatDialog
  ) {
    super();
  }

  openDialog(i: number, f?: FormlyFieldConfig) {
    const isEdit = !!f;
    const title = this.field.templateOptions.description;
    const dialogRef = this.dialog.open(RepeatSectionDialogComponent, {
      maxWidth: '100vw',
      maxHeight: '100vh',
      minWidth: '70vw',
      data: {
        title: isEdit ? title.replace(/^Add an|^Add a|^Add/, 'Edit') : title,
        fields: [this.field.fieldArray],
        model: isEdit ? this.field.fieldGroup[i].model : {},
      }
    });

    dialogRef.afterClosed().subscribe(data => {
      if (data && data.model) {
        if (super.formControl && super.formControl.controls.length > i) {
          super.remove(i);
        }

        super.add(i, data.model);

      }
    });
  }
}
