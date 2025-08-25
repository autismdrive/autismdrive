import {Component} from '@angular/core';
import {FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-mirror',
  templateUrl: './mirror.component.html',
  styleUrls: ['./mirror.component.scss'],
  imports: [FlexModule],
})
export class MirrorComponent {
  constructor() {}
}
