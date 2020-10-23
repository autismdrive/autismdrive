import {AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {FormControl} from '@angular/forms';
import {MatAutocomplete, MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {MatInput} from '@angular/material/input';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Observable, Subject, timer} from 'rxjs';
import {debounce, debounceTime, distinctUntilChanged, map, startWith} from 'rxjs/operators';
import {Category} from '../_models/category';
import {ApiService} from '../_services/api/api.service';
import {SearchService} from '../_services/api/search.service';

interface CategoriesById {
  [key: number]: Category;
}

interface CategoriesByDisplayOrder {
  [key: string]: Category;
}

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
  categoriesByDisplayOrder: CategoriesByDisplayOrder = {};
  categoriesById: CategoriesById = {};
  categoryTree: Category[];
  filteredOptions: Observable<Category[]>;
  options: Category[] = [];
  queryParams: Params;
  searchBoxControl = new FormControl();
  searchInputElement: MatInput;
  searchUpdate = new Subject<String>();
  skipUpdate = false;

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

    this.api.getCategoryTree().subscribe(categoryTree => {
      this.categoryTree = categoryTree;
      this._populateCategoryIndices(this.categoryTree);

      // Sort options by category level and display order
      this.options = Object
        .entries(this.categoriesByDisplayOrder) // each entry is an array containing [key, value]
        .sort((a, b) => a[0].toLowerCase() < b[0].toLowerCase() ? -1 : 1)
        .map(entry => entry[1]);

      this._populateCategoryParents();
      this.options.forEach(cat => {
        cat.indentedString = this.indentedString(cat);
      });
    });
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

  private _filter(value: string): Category[] {
    if (value && value.length > 0) {
      const words = value.replace(/\W+/gi, ' ').toLowerCase().split(' ');
      const patternString = words.map(w => `(?=.*${w})`).join('');
      const filterPattern = new RegExp(patternString, 'gi');
      return this.options.filter(option => option.all_resource_count > 0 && filterPattern.test(option.indentedString));
    } else {
      return this.options;
    }
  }

  /** Recursively walks the given category tree and puts each category into flattened indices for faster retrieval and sorting. */
  private _populateCategoryIndices(categoryTree: Category[], displayOrders = []) {
    // Index should be a string that can be sorted such that categories will be
    // in display order like this:
    // 0
    // 0.0
    // 0.0.0
    // 0.0.1
    // 0.1
    // 0.1.0
    // 0.0.1
    // ...
    // 1
    // 1.0
    // 1.0.0
    // ...etc...
    // so we want to add the ancestors' display orders into an array like this:
    // [0, 0, 1].join('.')

    // Walk the tree, pushing the ancestors display orders into the array as we go down.
    categoryTree.forEach(c => {
      const displayOrder = (c.display_order !== null && c.display_order !== undefined) ? c.display_order : c.id;
      const indexArray = displayOrders.concat([displayOrder]);
      const indexStr = indexArray.join('.');
      if (!this.categoriesByDisplayOrder[indexStr]) {
        this.categoriesByDisplayOrder[indexStr] = c;
      }
      if (!this.categoriesById[c.id]) {
        this.categoriesById[c.id] = c;
      }

      if (c.children && c.children.length > 0) {
        this._populateCategoryIndices(c.children, indexArray);
      }
    });
  }

  /** Adds the parent property to each of the categories in categoriesById */
  private _populateCategoryParents() {
    this.options.forEach(c => {
      if (c.parent_id !== null) {
        c.parent = this.categoriesById[c.parent_id];
        this.categoriesById[c.id].parent = c.parent;
      }
    });
  }
}
