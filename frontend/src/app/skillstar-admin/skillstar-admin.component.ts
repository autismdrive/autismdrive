import {Component} from '@angular/core';
import {ChainStep} from '@models/chain_step';
import {ApiService} from '@services/api/api.service';

@Component({
  selector: 'app-skillstar-admin',
  templateUrl: './skillstar-admin.component.html',
  styleUrls: ['./skillstar-admin.component.scss'],
})
export class SkillstarAdminComponent {
  chainSteps: ChainStep[] = [];

  constructor(private api: ApiService) {
    this.api.getChainStepsList().subscribe(cs => (this.chainSteps = cs));
  }

  get chainStepsText(): string {
    return this.chainSteps
      .sort((a, b) => a.id - b.id)
      .map(s => s.instruction)
      .join('\n');
  }

  save(formField: HTMLTextAreaElement) {
    console.log('formField', formField.value);
    const stepInstructions = formField.value.split('\n').map((instruction, id) => {
      const chainStep: ChainStep = {id, instruction};
      return chainStep;
    });

    stepInstructions.forEach(step => {
      if (step.instruction === '') {
        this.api.deleteChainStep(step).subscribe(
          result => {
            console.log('Delete blank step ID', step.id);
          },
          error => {
            console.error(`Cannot delete step ID ${step.id}`, error);
          },
        );
      } else {
        this.api.editChainStep(step).subscribe();
      }
    });
  }
}
