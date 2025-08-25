import {Component} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {ChainStep} from '@models/chain_step';
import {ApiService} from '@services/api/api.service';

@Component({
  standalone: true,
  selector: 'app-skillstar-admin',
  templateUrl: './skillstar-admin.component.html',
  styleUrls: ['./skillstar-admin.component.scss'],
  imports: [MatFormFieldModule, MatButtonModule, MatInputModule],
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
    const stepInstructions = formField.value.split('\n').map((instruction, id) => {
      const chainStep: ChainStep = {id, instruction};
      return chainStep;
    });

    stepInstructions.forEach(step => {
      if (step.instruction === '') {
        this.api.deleteChainStep(step).subscribe(
          _ => {},
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
