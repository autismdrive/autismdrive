import {Flow} from '@models/flow';
import {mockStep} from '@util/testing/fixtures/mock-step';

export const mockFlow: Flow = new Flow({
  name: 'self_intake',
  steps: [mockStep],
});
