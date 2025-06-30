import {Component} from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {FieldWrapper} from '@ngx-formly/core';

@Component({
  standalone: true,
  selector: 'app-card-wrapper',
  templateUrl: './card-wrapper.component.html',
  styleUrls: ['./card-wrapper.component.scss'],
  imports: [MatCardModule],
})
export class CardWrapperComponent extends FieldWrapper {}
