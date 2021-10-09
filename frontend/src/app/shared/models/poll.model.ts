import { User } from './user.model';

export enum PollStatus {
  VOTES_PENDING = 'votes pending',
  VOTES_RECEIVED = 'votes received',
  POLL_REVEALED = 'poll revealed',
}

export interface Poll {
  poll_id: string;
  description: string;
  owner_id: string;
  poll_status: PollStatus;
  participants: { [key: string]: User };
}
