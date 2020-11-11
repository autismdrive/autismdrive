import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  ViewChild
} from '@angular/core';
import {FormControl} from '@angular/forms';
import {MatAutocomplete, MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {MatInput} from '@angular/material/input';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Observable, Subject, timer} from 'rxjs';
import {debounce, debounceTime, distinctUntilChanged, map, startWith} from 'rxjs/operators';
import {Category} from '../_models/category';
import {ApiService} from '../_services/api/api.service';
import {CategoriesService} from '../_services/categories/categories.service';
import {SearchService} from '../_services/search/search.service';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.scss']
})
export class SearchBoxComponent implements OnInit, AfterViewInit {
  @Input() variant: string;
  @Input() words: string;
  @Output() categorySelected = new EventEmitter<Category>();
  @Output() searchUpdated = new EventEmitter<Params>();
  autocompletePanelElement: MatAutocomplete;
  filteredOptions: Observable<Category[]>;
  queryParams: Params;
  searchBoxControl = new FormControl();
  searchInputElement: MatInput;
  searchUpdate = new Subject<String>();
  skipUpdate = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService,
    private api: ApiService,
    private categoryService: CategoriesService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    this.route
      .queryParams
      .pipe(debounce(() => timer(1000)))
      .subscribe(qp => this.queryParams = qp);

    this.searchUpdate.pipe(
      debounceTime(400),
      distinctUntilChanged()
    ).subscribe(() => this.updateSearch(false));
  }

  get videoIsVisible(): boolean {
    return localStorage.getItem('shouldHideTutorialVideo') === 'true';
  }

  @ViewChild('searchInput', {read: MatInput})
  set searchInput(value: MatInput) {
    this.searchInputElement = value;
    this.searchInputElement.focus();
  }

  @ViewChild('autocompletePanel', {read: MatAutocomplete})
  set autocompletePanel(value: MatAutocomplete) {
    this.autocompletePanelElement = value;
  }

  get hasWords(): boolean {
    return !!(
      this.searchInputElement &&
      this.searchInputElement.value &&
      (this.searchInputElement.value.length > 0)
    );
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
        this.searchInputElement.value = q.words || this.words;
      }
    });
  }

  optionText(option: Category) {
    return option?.indentedString;
  }

  updateSearch(removeWords: boolean): Promise<boolean> {

    if (this.skipUpdate) {
      // Stupid hack to prevent submitting a keyword search when the user is selecting
      // a topic from the autocomplete panel.
      this.skipUpdate = false;
      return;
    }

    if (removeWords) {
      this.words = '';
      this.searchInputElement.value = this.words;
    }

    const newParams = JSON.parse(JSON.stringify(this.queryParams));
    const words: string = this.searchInputElement && this.searchInputElement.value || '';
    newParams.words = removeWords ? undefined : words;
    newParams.pageStart = 0;

    if (newParams.words) {
      newParams.sort = 'Relevance';
    }

    const hasFilters = Object.keys(newParams).length > 0;

    if (hasFilters) {
      return this.router.navigate(['/search'], {
        relativeTo: this.route,
        queryParams: newParams,
      }).finally(() => {
        this.searchUpdated.emit(newParams);
        this.changeDetectorRef.detectChanges();
      });
    } else {
      return this.router.navigateByUrl('/search').finally(() => this.searchUpdated.emit(newParams));
    }
  }

  /**
   * Returns a string of the given category's ancestors' names in the format:
   * "Grandparent Category Name > Parent Category Name > Category Name"
   */
  indentedString(option: Category) {
    let parent = option.parent;
    const parents = [];

    while (parent) {
      // Add ancestor to beginning of the parents array.
      parents.unshift(parent);

      // Go up to the next ancestor
      parent = parent.parent;
    }

    return parents
      .map(p => p.name)
      .concat([option.name])
      .join(' > ');
  }

  selectCategory($event: MatAutocompleteSelectedEvent) {
    // Stupid hack to prevent submitting a keyword search when the user is selecting
    // a topic from the autocomplete panel.
    this.skipUpdate = true;

    // Emit the selected category.
    this.categorySelected.emit($event.option.value as Category);
  }

  showVideo() {
    localStorage.removeItem('shouldHideTutorialVideo');
  }

  private _filter(value: string): Category[] {
    if (value && value.length > 0) {
      const words = value
        .replace(/\W+/gi, ' ')
        .toLowerCase()
        .split(' ');
      const patternString = words.map(w => `(?=.*${w})`).join('');
      const filterPattern = new RegExp(patternString, 'gi');
      return this.categoryService.categoryList
        .filter(option => {
          return (
            (option.all_resource_count > 0) &&
            filterPattern.test(option.indentedString)
          );
        });
    } else {
      return this.categoryService.categoryList;
    }
  }
}
