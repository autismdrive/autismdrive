import {Injectable} from '@angular/core';
import {CardWrapperComponent} from '@forms/card-wrapper/card-wrapper.component';
import {GroupValidationWrapperComponent} from '@forms/group-validation-wrapper/group-validation-wrapper.component';
import {HelpWrapperComponent} from '@forms/help-wrapper/help-wrapper.component';
import {MultiselectTreeComponent} from '@forms/multiselect-tree/multiselect-tree.component';
import {RepeatSectionComponent} from '@forms/repeat-section/repeat-section.component';
import {
  EmailMatchValidator,
  EmailMatchValidatorMessage,
  EmailValidator,
  EmailValidatorMessage,
  MaxValidationMessage,
  MinValidationMessage,
  MulticheckboxValidator,
  MulticheckboxValidatorMessage,
  PhoneValidator,
  PhoneValidatorMessage,
  ShowError,
  UrlValidator,
  UrlValidatorMessage,
} from '@forms/validators/formly.validator';

@Injectable()
export class FormlyConfig {
  public static config = {
    extras: {
      showError: ShowError,
    },
    types: [
      {name: 'repeat', component: RepeatSectionComponent},
      {
        name: 'multiselecttree',
        component: MultiselectTreeComponent,
        wrappers: ['card'],
      },
    ],
    validators: [
      {name: 'phone', validation: PhoneValidator},
      {name: 'email', validation: EmailValidator},
      {
        name: 'url',
        validation: UrlValidator,
      },
      {name: 'multicheckbox', validation: MulticheckboxValidator},
      {
        name: 'emailConfirm',
        validation: EmailMatchValidator,
      },
    ],
    validationMessages: [
      {name: 'phone', message: PhoneValidatorMessage},
      {
        name: 'email',
        message: EmailValidatorMessage,
      },
      {name: 'emailConfirm', message: EmailMatchValidatorMessage},
      {
        name: 'url',
        message: UrlValidatorMessage,
      },
      {name: 'multicheckbox', message: MulticheckboxValidatorMessage},
      {
        name: 'required',
        message: 'This field is required.',
      },
      {name: 'min', message: MinValidationMessage},
      {name: 'max', message: MaxValidationMessage},
    ],
    wrappers: [
      {name: 'help', component: HelpWrapperComponent},
      {
        name: 'card',
        component: CardWrapperComponent,
      },
      {name: 'group-validation', component: GroupValidationWrapperComponent},
    ],
  };
}
