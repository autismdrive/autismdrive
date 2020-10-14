import {AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {MatInput} from '@angular/material/input';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Observable, Subject, timer} from 'rxjs';
import {debounce, debounceTime, distinctUntilChanged, startWith, map} from 'rxjs/operators';
import {Category} from '../_models/category';
import {SearchService} from '../_services/api/search.service';
import {FormControl} from '@angular/forms';
import {ApiService} from '../_services/api/api.service';

interface CategoryMap { [key: number]: Category; }

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
  @Output() categorySelected = new EventEmitter<Category>();
  searchUpdate = new Subject<String>();
  searchBoxControl = new FormControl();
  options: Category[] = [];
  filteredOptions: Observable<Category[]>;
  categoryTree: Category[];
  flattenedCategoryTree: CategoryMap = {};

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
      console.log('category tree', categoryTree);
      this.categoryTree = categoryTree;
      const flattened = {};
      this._flattenCategoryTree(categoryTree, flattened);
      this.flattenedCategoryTree = this._flattenCategoryTree(categoryTree, flattened);
      this.options = Object.values(flattened);
      this._populateCategoryParents();
      console.log('flattened category tree', this.flattenedCategoryTree);
    });

    // this.api.getCategoryNamesList().subscribe(categories => {
    //   this.options = categories;
    // });
  }

  @ViewChild('searchInput', {read: MatInput, static: false})
  set searchInput(value: MatInput) {
    this.searchInputElement = value;
    this.searchInputElement.focus();
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

  private _filter(value: string): Category[] {
    const filterValue = value.toLowerCase();
    return this.options.filter(option => {
      const indentedString = (this.levelIndent(option) + ' ' + option.name);
      return indentedString.toLowerCase().includes(filterValue);
    });
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

  private _flattenCategoryTree(categoryTree: Category[], flattened: CategoryMap) {
    categoryTree.forEach(c => {
      if (!flattened[c.id]) { flattened[c.id] = c; }

      if (c.children && c.children.length > 0) {
        this._flattenCategoryTree(c.children, flattened);
      }
    });

    return flattened;
  }

  private _populateCategoryParents() {
    this.options.forEach(c => {
      if (c.parent_id !== null) {
        c.parent = this.flattenedCategoryTree[c.parent_id];
        this.flattenedCategoryTree[c.id].parent = c.parent;
      }
    });
  }

  levelIndent(option: Category) {
    let indentString = '';
    let parent = option.parent;

    while (parent) {
      indentString += `${parent.name} > `;
      parent = parent.parent;
    }

    return indentString;
  }

  selectCategory($event) {
    console.log('$event', $event);
    this.categorySelected.emit($event.option.value as Category);
  }
}
