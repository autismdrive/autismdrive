import {faker} from '@faker-js/faker';
import {AgeRange, Covid19Categories, Language} from '@models/hit_type';
import {UserFavorite} from '@models/user_favorite';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockResource} from '@util/testing/fixtures/mock-resource';
import {mockUser} from '@util/testing/fixtures/mock-user';

export const mockUserFavorite: UserFavorite = new UserFavorite({
  id: faker.number.int(),
  type: mockResource.type,
  user_id: mockUser.id,
  resource_id: mockResource.id,
  resource: mockResource,
  category_id: mockCategory.id,
  category: mockCategory,
  age_range: AgeRange.labels.adult,
  language: Language.labels.english,
  covid19_category: Covid19Categories.labels.Free_educational_resources,
  user: mockUser,
});
