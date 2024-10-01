import {faker} from '@faker-js/faker';
import {ChainStep} from '@models/chain_step';

export const mockChainStep: ChainStep = {
  id: faker.number.int(),
  name: faker.commerce.productName(),
  instruction: faker.commerce.productDescription(),
  last_updated: faker.date.recent(),
};
