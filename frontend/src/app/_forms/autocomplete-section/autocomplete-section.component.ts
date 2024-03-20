import {Component, OnInit} from '@angular/core';
import {FieldType} from '@ngx-formly/material';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';

@Component({
  selector: 'app-autocomplete-section',
  templateUrl: './autocomplete-section.component.html',
  styleUrls: ['./autocomplete-section.component.scss'],
})
export class AutocompleteSectionComponent extends FieldType implements OnInit {
  filteredOptions: Observable<any>;

  ngOnInit() {
    this.filteredOptions = this.formControl.valueChanges.pipe(
      startWith(''),
      map(value => (typeof value === 'string' ? value : value.name)),
      map(name => this.to.filter(name)),
    );
  }

  displayFn(option?: any): string | undefined {
    return option ? option.name : undefined;
  }
}
