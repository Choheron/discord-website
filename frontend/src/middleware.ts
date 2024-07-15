import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { verifyAuth, isMember } from './app/lib/discord_utils';
 
export async function middleware(request: NextRequest) {
  // Check if user is authorized, if not, redirect to login
  console.log("Ensuring user is logged in...");
  if(!(await verifyAuth())) {
    return NextResponse.redirect(new URL('/', request.url));
  }
  // Check if user is a member of the server, if not, redirect to homepage (As a way of ensuring no one mantually enters a url)
  // NOTE: This should run only if on a page that isnt publically accessible
  if((!request.nextUrl.pathname.match("/dashboard")) && (!await isMember())) {
    console.log("Ensuring user is member of server and is allowed to view the link...")
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  return;
}
 
// See "Matching Paths" below to learn more
export const config = {
  matcher: ['/dashboard', '/dashboard/:path*'],
}