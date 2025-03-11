import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {environment} from '@environments/environment';
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
import {ConfigService, ConfigServiceProps} from '@services/config/config.service';
import {lastValueFrom, of} from 'rxjs';
import {catchError} from 'rxjs/operators';

// Attempt to load the configuration from a file called config.json right next to
// this index page, it if exists. Otherwise, assume we are connecting to port
// 5000 on the local server.
export const load = (http: HttpClient, config: ConfigService): (() => Promise<boolean>) => {
  return async (): Promise<boolean> => {
    let url = './api/config';
    if ('override_config_url' in environment) {
      url = environment['override_config_url'];
    }

    let hasLocalConfig = false;

    // Check if a file called `config.json` is available in this file's directory.
    // If it is, load the configuration from there.
    try {
      const localConfig: ConfigServiceProps = await lastValueFrom(
        http.get<ConfigServiceProps>('./config.json', {responseType: 'json'}).pipe(
          catchError(() => {
            return of(null);
          }),
        ),
      );

      if (localConfig) {
        config.fromProperties(localConfig);
        hasLocalConfig = true;
      }
    } catch {
      hasLocalConfig = false;
    }

    if (hasLocalConfig) return hasLocalConfig;

    // Check with the backend to see if there is a configuration override available.
    try {
      const configFromJsonFile: ConfigServiceProps = await lastValueFrom(
        http.get<ConfigServiceProps>(url, {responseType: 'json'}).pipe(
          catchError(() => {
            return of(null);
          }),
        ),
      );
      if (configFromJsonFile) {
        config.fromProperties(configFromJsonFile);
      }
      return !!configFromJsonFile;
    } catch {
      return false;
    }
  };
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
