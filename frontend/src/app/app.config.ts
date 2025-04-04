import {HttpClient} from '@angular/common/http';
import {inject, Injectable} from '@angular/core';
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
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {ConfigService} from '@services/config/config.service';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';

// Attempt to load the configuration from a file called config.json right next to
// this index page, it if exists. Otherwise, assume we are connecting to port
// 5000 on the local server.
export const load = () => {
  inject(HttpClient);
  inject(ConfigService);
  inject(GoogleMapsLibraryService);
  inject(AuthenticationService)
  inject(ApiService)
};

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
