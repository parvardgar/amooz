import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = await req.json();

  const res = await fetch(`${process.env.DJANGO_API_URL}/accounts/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    credentials: "include", // important!
  });

  const data = await res.json();
  const response = NextResponse.json(data, { status: res.status });

  // Forward Django cookies to the browser
  const setCookie = res.headers.get("set-cookie");
  if (setCookie) {
    response.headers.set("set-cookie", setCookie);
  }

  return response;
}