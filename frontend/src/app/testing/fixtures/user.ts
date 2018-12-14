import { User } from '../../user';

export function getDummyUser(): User {
  return {
    id: 123,
    email: 'wicket@endor.gov',
    display_name: 'Wicket the Ewok',
    role: 'User'
  };
}
