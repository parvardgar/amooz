import "./globals.css";
import { AuthProvider } from "../context/AuthContext";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <p> This is from app/layout </p>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
