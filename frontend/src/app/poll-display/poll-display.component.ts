import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

import { Subscription } from 'rxjs';
import {
  WebsocketMessage,
  WebsocketMessageAction,
  WebsocketResponseType,
} from '../shared/models/messages.model';

import { Poll, PollStatus } from '../shared/models/poll.model';
import { User, VoteStatus } from '../shared/models/user.model';
import { PollApiService } from '../shared/services/poll-api.service';
import { PollMessageService } from '../shared/services/poll-message.service';

interface GroupedVote {
  name: string;
  userId: string;
}

@Component({
  selector: 'app-poll-display',
  templateUrl: './poll-display.component.html',
  styleUrls: ['./poll-display.component.css'],
})
export class PollDisplayComponent implements OnInit, OnDestroy {
  pollId: string | null = '';
  userId: string | null = '';
  pollLink: string = '';
  ownerId: string = '';
  poll: Poll | null = null;
  description: string = '';
  participants: User[] = [];
  pollStatus: PollStatus = PollStatus.VOTES_PENDING;
  myVoteStatus: VoteStatus = VoteStatus.PENDING;
  myVote: number | null = null;
  consensus: boolean = false;
  pollOptions: number[] = [0, 1, 2, 3, 5, 8, 13, 20, 40, 100];
  pollOptionsWithVotes: number[] = [];
  groupedVotes: GroupedVote[][] = [];

  subscriptions: Subscription[] = [];

  constructor(
    private route: ActivatedRoute,
    private pollApiService: PollApiService,
    private pollMessageService: PollMessageService,
    private snackBar: MatSnackBar
  ) {
    this.subscriptions.push(
      this.pollApiService.fetchPollSubject.subscribe((data) => {
        this.processPollData(data);
      })
    );
  }

  ngOnInit(): void {
    this.pollId = this.route.snapshot.paramMap.get('pollId');
    this.userId = this.route.snapshot.paramMap.get('userId');
    this.pollLink = `http://localhost/poll/${this.pollId}`

    this.pollApiService.fetchPoll(this.pollId as string, this.userId as string);

    this.pollMessageService.connect(
      this.pollId as string,
      this.userId as string
    );
    if (this.pollMessageService.messages) {
      this.subscriptions.push(
        this.pollMessageService.messages?.subscribe((data) => {
          if (data.response_type == WebsocketResponseType.UPDATE) {
            this.processPollData(data.poll as Poll);
          } else {
            console.log(data);
          }
        })
      );
    }
  }

  ngOnDestroy() {
    this.subscriptions.forEach((sub) => {
      sub.unsubscribe();
    });
  }

  processPollData(poll: Poll) {
    this.ownerId = poll.owner_id;
    this.description = poll.description;
    this.pollStatus = poll.poll_status;
    this.participants = Object.values(poll.participants);
    this.participants.forEach((element) => {
      if (element.user_id === this.userId) {
        this.myVote = element.vote || null;
        this.myVoteStatus = element.vote_status;
      }
    });

    if (this.pollStatus == PollStatus.POLL_REVEALED) {
      this.groupedVotes = [];
      this.pollOptionsWithVotes = [];

      for (let pollOption of this.pollOptions) {
        let newVoteGroup: GroupedVote[] = [];
        for (let participant of this.participants) {
          if (participant.vote == pollOption) {
            newVoteGroup.push({
              name: participant.name,
              userId: participant.user_id,
            });
          }
        }

        if (newVoteGroup.length > 0) {
          this.groupedVotes.push(newVoteGroup);
          this.pollOptionsWithVotes.push(pollOption);
        }
      }

      this.consensus = this.groupedVotes.length == 1;
    }
  }

  sendMessage(action: WebsocketMessageAction, vote?: number) {
    var message: WebsocketMessage = {
      action: action,
      poll_id: this.pollId as string,
      user_id: this.userId as string,
    };
    if (vote) {
      message.vote = vote;
    }
    this.pollMessageService.messages?.next(message);
  }

  submitVote(vote: number) {
    this.sendMessage(WebsocketMessageAction.CAST_VOTE, vote);
  }

  resetVote() {
    this.sendMessage(WebsocketMessageAction.RESET_VOTE);
  }

  revealPoll() {
    this.sendMessage(WebsocketMessageAction.REVEAL_POLL);
  }

  resetPoll() {
    this.sendMessage(WebsocketMessageAction.RESET_POLL);
  }

  showCopyLinkSnackbar() {
      let message = "Link copied";
      this.snackBar.open(message, undefined, {
          duration: 2000
      });


  }
}
