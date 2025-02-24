import {Component, Input} from '@angular/core';
import {RouterModule} from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-logo',
  templateUrl: './logo.component.html',
  styleUrls: ['./logo.component.scss'],
  imports: [RouterModule],
})
export class LogoComponent {
  @Input() variant?: string;

  constructor() {}
}
