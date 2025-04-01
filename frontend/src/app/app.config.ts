import {HttpClient} from '@angular/common/http';
import {inject, Injectable} from '@angular/core';
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
import {lastValueFrom} from 'rxjs';

// Attempt to load the configuration from a file called config.json right next to
// this index page, it if exists. Otherwise, assume we are connecting to port
// 5000 on the local server.
export const load = async (): Promise<ConfigServiceProps> => {
  console.log(`app.config.ts > load`);
  const httpClient = inject(HttpClient);
  const configService = inject(ConfigService);

  let url = './api/config';
  if ('override_config_url' in environment) {
    url = environment['override_config_url'];
  }

  let localConfig: ConfigServiceProps;

  // Check if a file called `config.json` is available in this file's directory.
  // If it is, load the configuration from there.
  try {
    localConfig = await lastValueFrom(httpClient.get<ConfigServiceProps>('./config.json', {responseType: 'json'}));
  } catch {
    localConfig = undefined;
  }

  if (localConfig) {
    console.log(`app.config.ts > load > localConfig: ${JSON.stringify(localConfig)}`);
    configService.fromProperties(localConfig);
    return localConfig;
  }

  // Check with the backend to see if there is a configuration override available.
  let configFromBackend: ConfigServiceProps;
  try {
    configFromBackend = await lastValueFrom(httpClient.get<ConfigServiceProps>(url, {responseType: 'json'}));
  } catch {
    configFromBackend = undefined;
  }

  if (configFromBackend) {
    console.log(`app.config.ts > load > configFromBackend: ${JSON.stringify(configFromBackend)}`);
    configService.fromProperties(configFromBackend);
    return configFromBackend;
  }
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
