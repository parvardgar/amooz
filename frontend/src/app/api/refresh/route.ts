import { NextResponse } from "next/server";

export async function POST() {
  const res = await fetch(`${process.env.DJANGO_API_URL}/api/token/refresh/`, {
    method: "POST",
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
