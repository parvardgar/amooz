import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const res = await fetch(`${process.env.DJANGO_API_URL}/accounts/auth/token/refresh`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        cookie: req.headers.get("cookie") || "",
      },
    credentials: "include", // send cookies
  });

  const data = await res.json();
  const response = NextResponse.json(data, { status: res.status });

  // forward cookies (updated access token)
  const setCookie = res.headers.get("set-cookie");
  if (setCookie) {
    response.headers.set("set-cookie", setCookie);
  }

  return response;
}
