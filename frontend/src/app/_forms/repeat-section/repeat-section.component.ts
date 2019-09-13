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
    const dialogRef = this.dialog.open(RepeatSectionDialogComponent, {
      width: `${window.innerWidth / 2}px`,
      data: {
        fields: [this.field.fieldArray],
        model: f ? this.field.fieldGroup[i].model : {},
      }
    });

    dialogRef.afterClosed().subscribe(data => {
      if (data && data.model) {
        console.log('data.model', data.model);
        super.remove(i);
        super.add(i, data.model);
      }
    });
  }
}
