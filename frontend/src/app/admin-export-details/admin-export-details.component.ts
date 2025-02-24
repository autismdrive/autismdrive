import {Component, Input} from '@angular/core';
import {MatTable, MatTableModule} from '@angular/material/table';
import {DataTransferDetail} from '@models/data_transfer_log';

@Component({
  standalone: true,
  selector: 'app-admin-export-details',
  templateUrl: './admin-export-details.component.html',
  styleUrls: ['./admin-export-details.component.scss'],
  imports: [MatTableModule],
})
export class AdminExportDetailsComponent {
  @Input() exportDetails: DataTransferDetail[];
  displayedColumns = ['class_name', 'successful', 'success_count', 'failure_count', 'errors'];

  constructor() {}
}
