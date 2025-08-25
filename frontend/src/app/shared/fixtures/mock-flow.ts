import {mockStep} from '@app/shared/fixtures/mock-step';
import {Flow} from '@models/flow';

export const mockFlow: Flow = new Flow({
  name: 'self_intake',
  steps: [mockStep],
});
