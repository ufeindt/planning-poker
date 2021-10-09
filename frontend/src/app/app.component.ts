import { Component } from '@angular/core';
import { PollMessageService } from './shared/services/poll-message.service';
import { WebsocketService } from './shared/services/websocket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [WebsocketService, PollMessageService]
})
export class AppComponent {
  title = 'Planning Poker';

  constructor(
    // private pollService: PollMessageService
    ) {
    // pollService.messages.subscribe(msg => {
    //   console.log("Response from websocket: " + msg);
    // });
  }

  // private message = {
  //   author: "tutorialedge",
  //   message: "this is a test message"
  // };

  // sendMsg() {
  //   console.log("new message from client to websocket: ", this.message);
  //   // this.pollService.messages.next(this.message);
  //   this.message.message = "";
  // }
}
