import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import {
  WebsocketMessage,
} from '../models/messages.model';
import { WebsocketService } from './websocket.service';

@Injectable({
  providedIn: 'root',
})
export class PollMessageService {
  public messages: Subject<WebsocketMessage> | null = null;

  constructor(private wsService: WebsocketService) {}

  connect(pollId: string, userId: string) {
    const websocketUrl = `${environment.websocket_host}/poll/${pollId}/user/${userId}`;
    this.messages = <Subject<WebsocketMessage>>(
      this.wsService.connect(websocketUrl).pipe(
        map((response: MessageEvent): WebsocketMessage => {
          let data = JSON.parse(response.data);
          console.log(data)
          return {
            response_type: data.response_type,
            message: data.message,
            poll: data.poll,
          };
        })
      )
    );
  }
}
