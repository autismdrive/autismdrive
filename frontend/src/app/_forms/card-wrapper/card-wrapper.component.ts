import {Component} from '@angular/core';
import {MatCard, MatCardContent, MatCardHeader} from '@angular/material/card';
import {FieldWrapper} from '@ngx-formly/core';

@Component({
  standalone: true,
  selector: 'app-card-wrapper',
  templateUrl: './card-wrapper.component.html',
  styleUrls: ['./card-wrapper.component.scss'],
  imports: [MatCard, MatCardHeader, MatCardContent],
})
export class CardWrapperComponent extends FieldWrapper {}
