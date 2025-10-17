// src/app/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    async function loadUser() {
      try {
        const res = await api.get("/profile"); // your Django or Next.js API route
        setUser(res.data);
      } catch (err) {
        console.error("Failed to load user:", err);
      }
    }
    loadUser();
  }, []);

  if (!user) return <p className="text-center mt-10">Loading...</p>;

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold">Welcome, {user.username}</h1>
    </div>
  );
}
