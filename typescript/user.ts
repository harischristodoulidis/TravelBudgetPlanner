export interface User {
  userId: string;
  username: string;
  passwordHash: string;
  firstName: string;
  lastName: string;
  friendIds: string[];
  createdAt: string;
}
