// src/app/api/me/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const res = await fetch(`${process.env.DJANGO_API_URL}/accounts/auth/me`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      cookie: req.headers.get("cookie") || "",
    },
    credentials: "include",
  });

  const data = await res.json();
  const response = NextResponse.json(data, { status: res.status });

  // forward cookies (if needed)
  const setCookie = res.headers.get("set-cookie");
  if (setCookie) response.headers.set("set-cookie", setCookie);

  return response;
}
