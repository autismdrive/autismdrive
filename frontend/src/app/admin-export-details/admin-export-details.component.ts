import {Component, Input} from '@angular/core';
import {DataTransferDetail} from '@models/data_transfer_log';

@Component({
  selector: 'app-admin-export-details',
  templateUrl: './admin-export-details.component.html',
  styleUrls: ['./admin-export-details.component.scss'],
})
export class AdminExportDetailsComponent {
  @Input() exportDetails: DataTransferDetail[];
  displayedColumns = ['class_name', 'successful', 'success_count', 'failure_count', 'errors'];

  constructor() {}
}
