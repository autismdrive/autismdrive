import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {StudyStatus, StudyStatusItem} from '@models/study';

@Component({
  standalone: true,
  selector: 'app-study-status-badge',
  imports: [MatIconModule, CommonModule],
  templateUrl: './study-status-badge.component.html',
  styleUrl: './study-status-badge.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudyStatusBadgeComponent {
  @Input() status: StudyStatusItem;

  snakeToKebab(str: string): string {
    return str.replace(/_/g, '-');
  }

  statusIcon(selectedStatus: StudyStatusItem): string {
    switch (selectedStatus.label) {
      case StudyStatus.currently_enrolling:
        return 'timer';
      case StudyStatus.study_in_progress:
        return 'psychology';
      case StudyStatus.results_being_analyzed:
        return 'query_stats';
      case StudyStatus.study_results_published:
        return 'assignment_turned_in';
      default:
        return '';
    }
  }
}
