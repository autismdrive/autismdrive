import {NgModule} from '@angular/core';
import {MockComponent} from '@app/shared/fixtures/mock.component';

@NgModule({
  imports: [MockComponent],
  exports: [MockComponent],
})
export class MockModule {}
