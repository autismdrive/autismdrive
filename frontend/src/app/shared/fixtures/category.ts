import {fake} from '@fixtures/fake';
import {Category} from '@models/category';

export const categoryFixtureFactory = (props: Partial<Category>): Category => {
  // Create a root-level category with default properties.
  const defaultProps: Category = {
    id: fake.number.int(),
    name: fake.word.words({count: {min: 1, max: 5}}),
    children: [],
    parent_id: null,
    parent: null,
    level: 0,
    all_resource_count: 0, // Calculated later
    resource_count: fake.number.int({min: 1, max: 1000}),
    event_count: fake.number.int({min: 1, max: 1000}),
    location_count: fake.number.int({min: 1, max: 1000}),
    study_count: fake.number.int({min: 1, max: 1000}),
    hit_count: 0, // Calculated later
    display_order: 0,
  };

  // Calculate the total count of all resources.
  defaultProps.all_resource_count =
    defaultProps.resource_count + defaultProps.event_count + defaultProps.location_count;

  // Calculate the total count of all search hits for this category.
  defaultProps.hit_count = defaultProps.all_resource_count + defaultProps.study_count;

  return props ? {...defaultProps, ...props} : defaultProps;
};

export interface NumCatsOptions {
  min: number;
  max: number;
}
export const numCatsOptions: NumCatsOptions = {min: 3, max: 7};

export const categoryWithChildrenFixtureFactory = (
  parentId: number | null,
  catParent: Category | null,
  index: number,
  level: number,
  options: NumCatsOptions = numCatsOptions,
) => {
  const catId = parseInt(`${parentId || 1}${index}`);
  const cat = categoryFixtureFactory({
    id: catId,
    parent_id: parentId,
    parent: catParent,
    level: level,

    // Calculate from last digit of the index
    display_order: index % 10,
  });

  if (level < 2) {
    cat.children = Array(fake.number.int(options))
      .fill(null)
      .map((_, i) => categoryWithChildrenFixtureFactory(catId, cat, i, level + 1));
  }

  return cat;
};

export const allCategoriesFixture = Array(fake.number.int(numCatsOptions))
  .fill(null)
  .map((_, i) => categoryWithChildrenFixtureFactory(null, null, i, 0));
