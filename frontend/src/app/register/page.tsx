"use client";

import { useState } from "react";

export default function SignupPage() {
  const [mobile, setMobile] = useState("");
  const [role, setRole] = useState<number | "">("");
  const [password, setPassword] = useState("");
  const [password_confirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState("");

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mobile, role, password, password_confirm }),
      credentials: "include",
    });

    if (res.ok) {
      window.location.href = "/profile"; // auto-login success
    } else {
      const data = await res.json();
      setError(data.error || "Signup failed");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSignup}
        className="bg-white p-6 rounded-2xl shadow-md w-80 space-y-4"
      >
        <h2 className="text-xl font-semibold text-center">Sign Up</h2>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <input
          type="text"
          placeholder="mobile"
          value={mobile}
          onChange={(e) => setMobile(e.target.value)}
          className="w-full p-2 border rounded-md"
        />
        <select
          value={role}
          onChange={(e) => setRole(parseInt(e.target.value, 10))}
          className="w-full p-2 border rounded-md"
        >
          <option value="">Select role</option>
          <option value={0}>Student</option>
          <option value={1}>Teacher</option>
        </select>
        <input 
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded-md"
        />
        <input
          type="password"
          placeholder="password confirm"
          value={password_confirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
          className="w-full p-2 border rounded-md"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
}
