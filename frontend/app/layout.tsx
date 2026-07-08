import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HireFlow - Candidate Screening System",
  description: "AI-assisted candidate screening and review workflows",
  icons: {
    icon: [{ url: "/icon.svg", type: "image/svg+xml" }],
  },
};

// Root layout wraps every page in the app.
// The <html> and <body> tags live here so Next.js can inject
// its own scripts and styles correctly.
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
