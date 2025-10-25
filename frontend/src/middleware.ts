export const runtime = "nodejs";

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import jwt, { JwtPayload } from "jsonwebtoken";

async function tryRefreshToken(req: NextRequest) {
  // call Next.js refresh API
  const refreshRes = await fetch(`${req.nextUrl.origin}/api/refresh`, {
    method: "POST",
    credentials: "include",
    headers: {
      cookie: req.headers.get("cookie") || "",
    },
  });
  return refreshRes.ok;
}

export async function middleware(req: NextRequest) {
  const access = req.cookies.get("access")?.value;
  const url = req.nextUrl.clone();
  if (!access) {
    // try refreshing immediately
    const refreshed = await tryRefreshToken(req);
    if (refreshed) return NextResponse.next();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  try {
    jwt.verify(access, process.env.JWT_SECRET!);
    return NextResponse.next();
  } catch (err: any) {
    if (err.name === "TokenExpiredError") {
      const refreshed = await tryRefreshToken(req);
      if (refreshed) return NextResponse.next();
    }
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }
}

export const config = {
  matcher: ["/dashboard/:path*", "/profile/:path*"],
};


// export const config = {
//   matcher: [
//     "/((?!api|_next|static|favicon.ico|login|signup|public).*)",
//   ],
// };