import {NgModule} from '@angular/core';
import {MockComponent} from '@util/testing/fixtures/mock.component';

@NgModule({
  declarations: [MockComponent],
  exports: [MockComponent],
})
export class MockModule {}
