export type User = {
  id?: number;
  username?: string;
  mobile?: string;
  role?: string;
  email?: string;
  // Add other profile fields your API returns
};

export type AuthState = {
  user: User | null;
  loading: boolean;       // true while initial fetch happening
  authenticated: boolean; // derived from user
};
