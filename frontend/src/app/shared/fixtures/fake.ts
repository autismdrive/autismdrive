import {base, en, en_US, Faker} from '@faker-js/faker';

export const fake = new Faker({locale: [en_US, en, base]});
