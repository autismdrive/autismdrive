import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { Training } from '../training';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-training-detail',
  templateUrl: './training-detail.component.html',
  styleUrls: ['./training-detail.component.scss']
})
export class TrainingDetailComponent implements OnInit {
  training: Training;

  constructor(private api: ApiService, private route: ActivatedRoute, private router: Router) {
    this.route.params.subscribe(params => {
      const trainingId = params.trainingId ? parseInt(params.trainingId, 10) : null;

      if (isFinite(trainingId)) {
        this.api.getTraining(trainingId).subscribe(training => {
          this.training = training;
        });
      }
    });
  }

  ngOnInit() {
  }

}
