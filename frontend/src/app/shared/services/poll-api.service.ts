import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Subject } from 'rxjs';

import { Poll } from '../models/poll.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PollApiService {
  public createPollSubject = new Subject<Poll>();
  public fetchPollSubject = new Subject<Poll>();
  public joinPollSubject = new Subject<string>();

  constructor(private http: HttpClient) {}

  createPoll(description: string, name: string) {
    var requestUrl = `${environment.api_host}/poll`;
    this.http
      .post<Poll>(
        requestUrl,
        { description: description, name: name }
      )
      .subscribe((data) => {
        this.createPollSubject.next(data);
      });
  }

  fetchPoll(pollId: string, userId?: string) {
    var requestUrl = `${environment.api_host}/poll/${pollId}`;
    if (userId) {
      requestUrl = `${requestUrl}/user/${userId}`;
    }

    this.http.get<Poll>(requestUrl).subscribe((data) => {
      this.fetchPollSubject.next(data);
    });
  }

  joinPoll(pollId: string, name: string) {
    var requestUrl = `${environment.api_host}/poll/${pollId}`;
    this.http
      .post<string>(requestUrl, { name: name })
      .subscribe((data) => {
        this.joinPollSubject.next(data);
      });
  }
}
