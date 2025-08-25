import {faker} from '@faker-js/faker';
import {Investigator} from '@models/investigator';

export const mockInvestigator: Investigator = {
  id: faker.number.int(),
  name: faker.person.fullName(),
  title: faker.person.jobTitle(),
  organization_name: faker.company.name(),
  bio_link: faker.internet.url(),
};
