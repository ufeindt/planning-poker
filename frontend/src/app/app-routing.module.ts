import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreatePollFormComponent } from './create-poll-form/create-poll-form.component';
import { JoinPollFormComponent } from './join-poll-form/join-poll-form.component';
import { PollDisplayComponent } from './poll-display/poll-display.component';

const routes: Routes = [
  { path: 'poll/:pollId/:userId', component: PollDisplayComponent },
  { path: 'poll/:pollId', component: JoinPollFormComponent },
  { path: 'poll', component: CreatePollFormComponent },
  { path: '', redirectTo: '/poll', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
