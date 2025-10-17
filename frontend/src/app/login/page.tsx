"use client";

import { useState } from "react";

export default function LoginPage() {
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mobile, password }),
      credentials: "include",
    });

    if (res.ok) {
      window.location.href = "/dashboard";
    } else {
      const data = await res.json();
      setError(data.error || "Login failed");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded-2xl shadow-md w-80 space-y-4"
      >
        <h2 className="text-xl font-semibold text-center">Login</h2>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <input
          type="text"
          placeholder="mobile"
          value={mobile}
          onChange={(e) => setMobile(e.target.value)}
          className="w-full p-2 border rounded-md"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded-md"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
        >
          Login
        </button>
      </form>
    </div>
  );
}
