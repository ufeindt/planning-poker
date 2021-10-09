export enum VoteStatus {
  PENDING = 'pending',
  VOTED = 'voted',
}

export interface User {
  user_id: string;
  name: string;
  vote?: number;
  vote_status: VoteStatus;
}
