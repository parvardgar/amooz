const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface LoginData {
  mobile: string;
  password: string;
}

interface SignupData {
  mobile: string;
  role: number;
  password: string;
  password_confirm: string;
}

interface LogoutData {
  token: string;
}

interface AuthResponse {
  token: string;
  user: {
    id: number;
    mobile: string;
    role: number;
  };
}

export class ApiService {
  private static async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('Making API request to:', url); // Debug log
    console.log('Request options:', options); // Debug log
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();
      console.log('Response status:', response.status); // Debug log
      if (!response.ok) {
        throw new Error(data.message || 'Something went wrong');
      }

      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Network error occurred');
    }
  }

  static async login(loginData: LoginData): Promise<AuthResponse> {
    return this.request<AuthResponse>('/accounts/auth/login', {
      method: 'POST',
      body: JSON.stringify(loginData),
    });
  }

  static async signup(signupData: SignupData): Promise<AuthResponse> {
    return this.request<AuthResponse>('/accounts/auth/register', {
      method: 'POST',
      body: JSON.stringify(signupData),
    });
  }

  static async logout(logoutData: LogoutData): Promise<void> {
    return this.request<void>('/accounts/auth/logout', {
      method: 'POST',
      body: JSON.stringify(logoutData),
    });
  }
}