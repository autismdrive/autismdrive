import {
  allCategoriesFixture,
  categoryFixtureFactory,
  categoryWithChildrenFixtureFactory,
  numCatsOptions,
} from '@fixtures/category';
import {Category} from '@models/category';

describe('Category Fixture Factories', () => {
  const expectCategoryPropertiesToBeDefined = (category: Category) => {
    ['id', 'name', 'children', 'level', 'display_order'].forEach(prop => expect(category[prop]).toBeDefined());

    ['all_resource_count', 'resource_count', 'event_count', 'location_count', 'study_count', 'hit_count'].forEach(
      prop => expect(category[prop]).toBeGreaterThan(0),
    );
  };

  const expectChildrenToBeDefined = (
    category: Category,
    parentId: number | null,
    level: number,
    minChildren: number,
    maxChildren: number,
  ) => {
    it(`should have ${minChildren}-${maxChildren} children for level ${level} category`, () => {
      expect(category.parent_id).toEqual(parentId);
      expect(category.level).toEqual(level);
      expect(category.children.length).toBeGreaterThanOrEqual(minChildren);
      expect(category.children.length).toBeLessThanOrEqual(maxChildren);
      expectCategoryPropertiesToBeDefined(category);
    });

    category.children.forEach(child => {
      const _min = level < 1 ? minChildren : 0;
      const _max = level < 1 ? maxChildren : 0;
      expectChildrenToBeDefined(child, category.id, level + 1, _min, _max);
    });
  };

  it('should create a root-level category with default properties', () => {
    const category = categoryFixtureFactory({});
    expect(category).toBeDefined();
    expect(category.parent_id).toBeNull();
    expect(category.level).toEqual(0);
    expectCategoryPropertiesToBeDefined(category);
    expect(category.children.length).toEqual(0);
  });

  describe('should create a single category with children', () => {
    const options = {min: 2, max: 9};
    const category = categoryWithChildrenFixtureFactory(null, null, 1, 0, options);
    expectChildrenToBeDefined(category, null, 0, options.min, options.max);
  });

  describe('should create multiple categories with children', () => {
    allCategoriesFixture.forEach(cat => {
      expectChildrenToBeDefined(cat, null, 0, numCatsOptions.min, numCatsOptions.max);
    });

    it('should be exactly 3 levels deep', () => {
      allCategoriesFixture.forEach(cat => {
        const checkDepth = (category: Category, depth: number = 0) => {
          expect(depth).toBeLessThanOrEqual(3);
          category.children.forEach(child => checkDepth(child, depth + 1));
        };
        checkDepth(cat);
      });
    });
  });
});
