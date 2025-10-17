// src/lib/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "/api",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

// Simple single-refresh lock to avoid multiple /api/refresh calls
let isRefreshing = false;
let failedQueue: Array<{ resolve: (value?: any) => void; reject: (error: any) => void; config: any }> = [];

const processQueue = (error: any, tokenUpdated = false) => {
  failedQueue.forEach((p) => {
    if (error) p.reject(error);
    else p.resolve(tokenUpdated);
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    // If the request has no config (e.g., network failure), just reject
    if (!originalRequest) return Promise.reject(error);

    // If 401 and not retrying already
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // queue the request until refresh completes
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject, config: originalRequest });
        }).then(() => api(originalRequest));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshRes = await axios.post("/api/refresh", {}, { withCredentials: true });
        // refresh succeeded, process the queue
        processQueue(null, true);
        isRefreshing = false;
        return api(originalRequest); // retry original
      } catch (err) {
        processQueue(err, false);
        isRefreshing = false;
        // optional: redirect to login here
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
