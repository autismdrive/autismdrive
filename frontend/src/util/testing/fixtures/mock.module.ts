import {NgModule} from '@angular/core';
import {MockComponent} from '@util/testing/fixtures/mock.component';

@NgModule({
  imports: [MockComponent],
  exports: [MockComponent],
})
export class MockModule {}
