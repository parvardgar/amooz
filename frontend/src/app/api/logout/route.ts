import { NextResponse } from "next/server";

export async function POST() {
  const res = await fetch(`${process.env.DJANGO_API_URL}/api/logout/`, {
    method: "POST",
    credentials: "include",
  });

  const response = NextResponse.json(await res.json(), { status: res.status });
  response.headers.set(
    "set-cookie",
    "access=; Max-Age=0; path=/, refresh=; Max-Age=0; path=/"
  );
  return response;
}
