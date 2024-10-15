import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {CategoriesById, Category} from '@models/category';
import {CategoriesService} from '@services/categories/categories.service';

@Component({
  selector: 'app-search-topics',
  templateUrl: './search-topics.component.html',
  styleUrls: ['./search-topics.component.scss'],
})
export class SearchTopicsComponent {
  @Input() category: Category;
  @Output() categorySelected = new EventEmitter<Category>();
  categoriesById: CategoriesById = {};
  loading = true;

  constructor(
    private categoriesService: CategoriesService,
    private changeDetectorRef: ChangeDetectorRef,
  ) {
    if (this.categoriesService.categoriesById) {
      this.categoriesById = this.categoriesService.categoriesById;
      this.loading = false;
    }

    this.categoriesService.updated.subscribe(() => {
      this.categoriesById = this.categoriesService.categoriesById;
      this.loading = false;
      this.changeDetectorRef.detectChanges();
    });
  }

  get categories() {
    return this.getChildrenWithHits(this.category);
  }

  selectCategory(cat: Category) {
    this.categorySelected.emit(cat);
  }

  parentList(current: Category = this.category, parents: any[] = []): any[] {
    if (current.parent) {
      parents.unshift(current.parent);
      return this.parentList(current.parent, parents);
    } else {
      return parents;
    }
  }

  hasChildren(cat: Category) {
    const category = cat.id === null ? cat : this.categoriesById[cat.id];
    return category && category.children && category.children.length > 0;
  }

  getChildrenWithHits(cat: Category) {
    if (this.hasChildren(cat)) {
      return cat.children.filter(c => c.hit_count > 0);
    } else {
      return [];
    }
  }
}
