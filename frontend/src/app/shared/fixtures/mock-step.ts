import {faker} from '@faker-js/faker';
import {Step, StepStatus, StepType} from '@models/step';

export const makeMockStep = (overrides?: Partial<Step>): Step => {
  overrides = overrides || {};
  const defaults: Step = {
    name: faker.commerce.productName(),
    type: StepType.SENSITIVE,
    description: faker.commerce.productDescription(),
    label: faker.commerce.product(),
    status: StepStatus.INCOMPLETE,
    date_completed: faker.date.recent(),
    questionnaire_id: faker.number.int(),
  };

  return {...defaults, ...overrides};
};

export const mockStep = makeMockStep();
