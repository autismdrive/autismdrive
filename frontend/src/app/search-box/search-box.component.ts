import {AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {MatInput} from '@angular/material/input';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Observable, Subject, timer} from 'rxjs';
import {debounce, debounceTime, distinctUntilChanged, startWith, map} from 'rxjs/operators';
import {SearchService} from '../_services/api/search.service';
import {FormControl} from '@angular/forms';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.scss']
})
export class SearchBoxComponent implements OnInit, AfterViewInit {
  searchInputElement: MatInput;
  queryParams: Params;
  @Input() words: string;
  @Input() variant: string;
  @Output() searchUpdated = new EventEmitter<Params>();
  searchUpdate = new Subject<String>();
  searchBoxControl = new FormControl();
  options: string[] = [];
  filteredOptions: Observable<string[]>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService,
    private api: ApiService
  ) {
    this.route
      .queryParams
      .pipe(debounce(() => timer(1000)))
      .subscribe(qp => this.queryParams = qp);
    this.searchUpdate.pipe(
      debounceTime(400),
      distinctUntilChanged()
    ).subscribe(value => this.updateSearch(false));

    this.api.getCategoryNamesList().subscribe(categories => {
      this.options = categories;
    });
  }

  @ViewChild('searchInput', {read: MatInput, static: false})
  set searchInput(value: MatInput) {
    this.searchInputElement = value;
  }

  ngOnInit() {
    this.filteredOptions = this.searchBoxControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
  }

  ngAfterViewInit() {
    this.searchService.currentQuery.subscribe(q => {
      if (q === null || (q && q.hasOwnProperty('words') && q.words === '')) {
        if (this.searchInputElement) {
          this.searchInputElement.value = '';
        }
      } else {
        console.log('q.words', q.words);
        this.searchInputElement.value = q.words || this.words;
      }
    });
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }
  updateSearch(removeWords: boolean): Promise<boolean> {
    if (removeWords) {
      this.words = '';
      this.searchInputElement.value = this.words;
    }

    const newParams = JSON.parse(JSON.stringify(this.queryParams));
    const words: string = this.searchInputElement && this.searchInputElement.value || '';
    newParams.words = removeWords ? undefined : words;
    const hasFilters = Object.keys(newParams).length > 0;

    if (hasFilters) {
      return this.router.navigate(['/search'], {
        relativeTo: this.route,
        queryParams: newParams,
      }).finally(() => this.searchUpdated.emit(newParams));
    } else {
      return this.router.navigateByUrl('/search').finally(() => this.searchUpdated.emit(newParams));
    }
  }

  hasWords(): boolean {
    return this.searchInputElement && this.searchInputElement.value && (this.searchInputElement.value.length > 0);
  }

}
