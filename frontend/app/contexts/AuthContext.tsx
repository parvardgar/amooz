'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ApiService } from '../library/api';

interface User {
  id: number;
  mobile: string;
  role: number;
}

interface AuthContextType {
  user: User | null;
  login: (mobile: string, password: string) => Promise<void>;
  signup: (
    mobile: string,
    role: number,
    password: string,
    password_confirm: string,
  ) => Promise<void>;
  logout: (token: string) => void;
  isLoading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    
    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (e) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
      }
    }
  }, []);

  const login = async (mobile: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await ApiService.login({ mobile, password });
      
      // Store token and user data
      localStorage.setItem('auth_token', response.token);
      localStorage.setItem('user_data', JSON.stringify(response.user));
      setUser(response.user);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (
    mobile: string,
    role: number,
    password: string,
    password_confirm: string,
    
  ) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await ApiService.signup({
        mobile,
        role, 
        password, 
        password_confirm
      });
      
      // Store token and user data
      localStorage.setItem('auth_token', response.token);
      localStorage.setItem('user_data', JSON.stringify(response.user));
      setUser(response.user);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Signup failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = (token: string) => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    setUser(null);
    // Optionally call logout endpoint
    ApiService.logout({token}).catch(console.error);
  };

  const value = {
    user,
    login,
    signup,
    logout,
    isLoading,
    error,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}