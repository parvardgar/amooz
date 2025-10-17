// src/context/AuthContext.tsx
"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import api from "@/lib/api";
import type { User } from "./auth.types";

type AuthContextValue = {
  user: User | null;
  loading: boolean;
  authenticated: boolean;
  login: (credentials: { mobile: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<boolean>;
  fetchUser: () => Promise<User | null>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch current user from backend
  const fetchUser = useCallback(async (): Promise<User | null> => {
    try {
      const res = await api.get("/profile");
      setUser(res.data);
      return res.data;
    } catch (err) {
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  // Refresh tokens via /api/refresh; returns true if refreshed successfully
  const refresh = useCallback(async (): Promise<boolean> => {
    try {
      const res = await api.post("/refresh");
      return res.status === 200;
    } catch (err) {
      setUser(null);
      return false;
    }
  }, []);

  // Login (calls /api/login) — credentials sent, cookies set server-side
  const login = useCallback(async (credentials: { mobile: string; password: string }) => {
    setLoading(true);
    try {
      await api.post("/login", credentials); // Django will set cookies
      // immediately fetch user profile
      await fetchUser();
    } catch (err) {
      setUser(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchUser]);

  // Logout
  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await api.post("/logout");
      setUser(null);
      // Optionally redirect to login
      if (typeof window !== "undefined") window.location.href = "/login";
    } catch (err) {
      console.error("Logout failed", err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial mount: fetch user (and attempt refresh if needed)
  useEffect(() => {
    let mounted = true;

    (async () => {
      try {
        // Try to fetch user first
        const u = await fetchUser();
        if (!u) {
          // if no user, try refresh once and try fetching again
          const refreshed = await refresh();
          if (refreshed) {
            await fetchUser();
          }
        }
      } catch (err) {
        console.error("Auth init error", err);
      } finally {
        if (mounted) setLoading(false);
      }
    })();

    return () => {
      mounted = false;
    };
  }, [fetchUser, refresh]);

  // Background refresh: periodically refresh access token
  useEffect(() => {
    // run only when authenticated (user exists)
    if (!user) return;

    const interval = setInterval(async () => {
      try {
        await refresh();
      } catch (err) {
        console.warn("Background refresh failed", err);
      }
    }, 4 * 60 * 1000); // every 4 minutes (adjust to your access token lifetime)

    return () => clearInterval(interval);
  }, [user, refresh]);

  const value: AuthContextValue = {
    user,
    loading,
    authenticated: !!user,
    login,
    logout,
    refresh,
    fetchUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
