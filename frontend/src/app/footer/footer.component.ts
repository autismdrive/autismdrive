import {Component} from '@angular/core';
import {NgIf} from '@angular/common';
import {Router} from '@angular/router';
import {ConfigService} from '@services/config/config.service';

@Component({
  standalone: true,
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
  imports: [NgIf],
})
export class FooterComponent {
  constructor(
    public config: ConfigService,
    public router: Router,
  ) {}
}
