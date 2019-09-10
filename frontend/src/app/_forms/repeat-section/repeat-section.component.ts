import {Component} from '@angular/core';
import {FieldArrayType, FormlyFieldConfig, FormlyFormBuilder} from '@ngx-formly/core';
import {MatDialog} from '@angular/material/dialog';
import {RepeatSectionDialogComponent} from '../repeat-section-dialog/repeat-section-dialog.component';

@Component({
  selector: 'app-repeat-section',
  templateUrl: './repeat-section.component.html',
  styleUrls: ['./repeat-section.component.scss']
})
export class RepeatSectionComponent extends FieldArrayType {
  constructor(
    builder: FormlyFormBuilder,
    public dialog: MatDialog
  ) {
    super(builder);
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
        super.remove(i);
        super.add(i, data.model);
      }
    });
  }

  displayValues(f: FormlyFieldConfig) {
    return Object.keys(f.model).forEach(k => { return {key: k, value: f.model[k]}; });
  }
}
