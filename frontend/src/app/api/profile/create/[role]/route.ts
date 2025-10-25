// src/app/api/[role]/profiles/route.ts

import { NextRequest, NextResponse } from "next/server";

// Handle POST (profile creation)
export async function POST(req: NextRequest, { params }: { params: { role: string } }) {
  const { role } = params; // "student" | "teacher" | "parent"
  const body = await req.json();

  // Validate the role to avoid security issues
  if (!["student", "teacher", "parent"].includes(role)) {
    return NextResponse.json({ error: "Invalid role" }, { status: 400 });
  }

  try {
    // Forward the request to your Django backend
    const res = await fetch(`${process.env.DJANGO_API_URL}/accounts/auth/create/${role}/profile`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        cookie: req.headers.get("cookie") || "",
      },
      body: JSON.stringify(body),
      credentials: "include", // ensure cookies go through
    });

    const data = await res.json();
    const response = NextResponse.json(data, { status: res.status });

    // Forward any cookies Django sent (for auth)
    const setCookie = res.headers.get("set-cookie");
    if (setCookie) {
      response.headers.set("set-cookie", setCookie);
    }

    return response;
  } catch (error) {
    console.error("Profile creation failed:", error);
    return NextResponse.json({ error: "Profile creation failed" }, { status: 500 });
  }
}




// import { proxyToDjango } from "@/lib/proxyToDjango";

// export async function POST(req: NextRequest, { params }: { params: { role: string } }) {
//   const { role } = params;
//   const body = await req.json();

//   if (!["student", "teacher", "parent"].includes(role))
//     return NextResponse.json({ error: "Invalid role" }, { status: 400 });

//   return proxyToDjango(req, `/${role}/profiles/`, "POST", body);
// }