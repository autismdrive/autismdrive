import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {LocationDialogData} from '../_models/location_dialog_data';

@Component({
  selector: 'app-set-location-dialog',
  templateUrl: './set-location-dialog.component.html',
  styleUrls: ['./set-location-dialog.component.scss']
})
export class SetLocationDialogComponent {

  constructor(
    public dialogRef: MatDialogRef<SetLocationDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: LocationDialogData
  ) {
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    localStorage.setItem('zipCode', this.data.zipCode);
    this.dialogRef.close();
  }

}
