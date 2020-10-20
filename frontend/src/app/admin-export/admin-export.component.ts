import {Component, ComponentFactory, ComponentFactoryResolver, OnInit, ViewChild, ViewChildren, ViewContainerRef} from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {ApiService} from '../_services/api/api.service';
import {Router} from '@angular/router';
import {tap} from 'rxjs/operators';
import {DataTransferDataSource} from '../_models/data_transfer_data_source';
import { merge } from 'rxjs/internal/observable/merge';
import {AdminExportDetailsComponent} from '../admin-export-details/admin-export-details.component';
import {DataTransferLog} from '../_models/data_transfer_log';
import {ConfigService} from '../_services/config.service';

@Component({
  selector: 'app-admin-export',
  templateUrl: './admin-export.component.html',
  styleUrls: ['./admin-export.component.scss']
})
export class AdminExportComponent implements OnInit {
  dataTransferDataSource: DataTransferDataSource;
  columns = [];
  default_page_size = 10;
  mirroring: boolean;
  count = 0;
  expandedRow: number;
  latestLog: DataTransferLog;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
  @ViewChildren('tableRow', { read: ViewContainerRef }) rowContainers;

  constructor(
    private api: ApiService,
    private configService: ConfigService,
    private router: Router,
    private resolver: ComponentFactoryResolver
  ) {}

  ngOnInit(): void {
    this.mirroring = this.configService.mirroring;
    this.loadData();
    this.loadLatestLog();
    merge(this.paginator.page).pipe(
      tap(() => this.loadData())
    ).subscribe();
  }

  loadData() {
      this.dataTransferDataSource = new DataTransferDataSource(this.api);
      this.columns = ['id', 'type', 'date_started', 'last_updated', 'total_records', 'alerts_sent'];
      this.dataTransferDataSource.loadLogs(this.paginator.pageIndex, this.paginator.pageSize);
      this.dataTransferDataSource.count$.subscribe(c => {this.count = c; });
  }

  getRowClass(log: DataTransferLog) {
    if (log.details.filter(d => !d.successful).length > 0) {
      return 'error';
    }
    if (log.alerts_sent > 0) {
      return 'warn';
    }
    return 'normal';
  }

  loadLatestLog() {
    this.api.getDataTransferLogs(0, 1).subscribe(pages => {
      if (pages.items.length > 0) {
        this.latestLog = pages.items[0];
      }
    });
  }

  selectRow(index: number) {
    console.log('Row ' + index + ' Selected');
    if (this.expandedRow != null) {
      // clear old content
      this.rowContainers.toArray()[this.expandedRow].clear();
    }

    if (this.expandedRow === index) {
      this.expandedRow = null;
    } else {
      const container = this.rowContainers.toArray()[index];
      const factory: ComponentFactory<any> = this.resolver.resolveComponentFactory(AdminExportDetailsComponent);
      const inlineComponent = container.createComponent(factory);
      this.dataTransferDataSource.logs$.subscribe(logs => {
        inlineComponent.instance.exportDetails = logs[index].details;
        this.expandedRow = index;
      });
    }
  }
}
