// src/lib/proxyToDjango.ts
import { NextRequest, NextResponse } from "next/server";

export async function proxyToDjango(
  req: NextRequest,
  djangoPath: string,
  method: string = "GET",
  body?: any
) {
  const res = await fetch(`${process.env.DJANGO_API_URL}${djangoPath}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      cookie: req.headers.get("cookie") || "",
    },
    body: body ? JSON.stringify(body) : undefined,
    credentials: "include",
  });

  const data = await res.json();
  const response = NextResponse.json(data, { status: res.status });

  const setCookie = res.headers.get("set-cookie");
  if (setCookie) response.headers.set("set-cookie", setCookie);

  return response;
}
