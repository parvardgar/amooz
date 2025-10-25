"use client";

import { useState } from "react";

import { UserRole } from "../../constants/roles";

export default function SignupPage() {
  const [mobile, setMobile] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
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
      body: JSON.stringify({
        mobile, first_name, last_name,
        role, password, password_confirm 
      }),
      credentials: "include",
    });

    if (res.ok) {
      let redirectUrl = "/profile";
      switch (role) {
        case UserRole.Student:
          redirectUrl = "/profile/create/student";
          break;
        case UserRole.Teacher:
          redirectUrl = "/profile/create/teacher";
          break;
        case UserRole.Parent:
          redirectUrl = "/profile/create/parent";
          break;
      }
      window.location.href = redirectUrl;
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
        <input
          type="text"
          placeholder="first name"
          value={first_name}
          onChange={(e) => setFirstName(e.target.value)}
          className="w-full p-2 border rounded-md"
        />
        <input
          type="text"
          placeholder="last name"
          value={last_name}
          onChange={(e) => setLastName(e.target.value)}
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
          <option value={2}>Parent</option>
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
