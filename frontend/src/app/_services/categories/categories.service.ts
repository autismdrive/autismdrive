import {EventEmitter, Injectable, Output} from '@angular/core';
import {CategoriesByDisplayOrder, CategoriesById, Category} from '@models/category';
import {ApiService} from '../api/api.service';

@Injectable({
  providedIn: 'root',
})
export class CategoriesService {
  categoryTree: Category[];
  categoryList: Category[];
  categoriesByDisplayOrder: CategoriesByDisplayOrder = {};
  categoriesById: CategoriesById = {};
  @Output() updated = new EventEmitter<boolean>();

  constructor(private api: ApiService) {
    this.api.getCategoryTree().subscribe(categoryTree => {
      this.categoryTree = categoryTree;
      this._populateCategoryIndices(this.categoryTree);

      // Sort options by category level and display order
      this.categoryList = Object.entries(this.categoriesByDisplayOrder) // each entry is an array containing [key, value]
        .sort((a, b) => (a[0].toLowerCase() < b[0].toLowerCase() ? -1 : 1))
        .map(entry => entry[1]);

      this._populateCategoryParents();
      this.categoryList.forEach(cat => {
        cat.indentedString = this._indentedString(cat);
      });

      this.updated.emit(true);
    });
  }

  /**
   * Returns a string of the given category's ancestors' names in the format:
   * "Grandparent Category Name > Parent Category Name > Category Name"
   */
  private _indentedString(option: Category) {
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
      const displayOrder = c.display_order !== null && c.display_order !== undefined ? c.display_order : c.id;
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
    this.categoryList.forEach(c => {
      if (c.parent_id !== null) {
        c.parent = this.categoriesById[c.parent_id];
        this.categoriesById[c.id].parent = c.parent;
      }
    });
  }
}
