import {Component, Input} from '@angular/core';
import {RouterLink} from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-logo',
  templateUrl: './logo.component.html',
  styleUrls: ['./logo.component.scss'],
  imports: [RouterLink],
})
export class LogoComponent {
  @Input() variant?: string;

  constructor() {}
}
