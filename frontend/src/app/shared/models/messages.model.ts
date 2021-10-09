import { Poll } from './poll.model';

export enum WebsocketMessageAction {
  CAST_VOTE = 'cast vote',
  RESET_VOTE = 'reset vote',
  RESET_POLL = 'reset poll',
  REVEAL_POLL = 'reveal poll',
}


export enum WebsocketResponseType {
  ERROR = 'error',
  UPDATE = 'update',
}

export interface WebsocketMessage {
  poll_id?: string;
  user_id?: string;
  action?: WebsocketMessageAction;
  vote?: number;
  response_type?: WebsocketResponseType;
  message?: string;
  poll?: Poll;
}
