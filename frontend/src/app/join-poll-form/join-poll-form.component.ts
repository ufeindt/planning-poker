import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { PollApiService } from '../shared/services/poll-api.service';

@Component({
  selector: 'app-join-poll-form',
  templateUrl: './join-poll-form.component.html',
  styleUrls: ['./join-poll-form.component.css'],
})
export class JoinPollFormComponent implements OnInit, OnDestroy {
  pollId: string | null = '';
  name: string = '';

  subscriptions: Subscription[] = [];

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private pollApiService: PollApiService
  ) {
    this.subscriptions.push(
      this.pollApiService.joinPollSubject.subscribe((data) => {
        this.router.navigate(['poll', this.pollId, data]);
      })
    );
  }

  ngOnInit(): void {
    this.pollId = this.route.snapshot.paramMap.get('pollId');
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach((sub) => {
      sub.unsubscribe();
    });
  }

  submitForm(): void {
    if (this.pollId) {
      this.pollApiService.joinPoll(this.pollId, this.name);
    }
  }
}
