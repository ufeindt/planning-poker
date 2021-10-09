import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { PollApiService } from '../shared/services/poll-api.service';

@Component({
  selector: 'app-create-poll-form',
  templateUrl: './create-poll-form.component.html',
  styleUrls: ['./create-poll-form.component.css'],
})
export class CreatePollFormComponent implements OnInit, OnDestroy {
  description: string = "";
  name: string = "";

  subscriptions: Subscription[] = [];

  constructor(private router: Router,
    private pollApiService: PollApiService) {
    this.subscriptions.push(
      this.pollApiService.createPollSubject.subscribe((data) => {
        this.router.navigate(['poll', data.poll_id, data.owner_id])
      })
    );
  }

  ngOnInit(): void {}

  ngOnDestroy(): void {
    this.subscriptions.forEach((sub) => {
      sub.unsubscribe();
    });
  }

  submitForm(): void {
    this.pollApiService.createPoll(this.description, this.name);
  }
}
