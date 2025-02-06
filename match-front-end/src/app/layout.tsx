import Link from "next/link";
import type { Metadata } from "next";
import Head from "next/head";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Melody Match",
  description: "Your guide in the world of music",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <Head>
        <link rel="icon" type="image/png" href="/audio-waves.png" sizes="any" />
      </Head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="bg-custom-gradient bg-fixed bg-cover min-h-screen">
          <div className="h-20 flex items-center px-12 py-2 z-10">
            <Link
              href="/"
              className="flex items-center gap-[10px] no-underline"
            >
              <img
                src="/audio-waves.png"
                alt="Melody Match Logo"
                className="h-[60px] w-auto"
              />
              <h2 className="m-0 text-[36px] font-black animate-gradient">
                melody_match
              </h2>
            </Link>
          </div>
          {children}
        </div>
        {/* footer */}
        <footer className="pt-12 text-center text-white text-sm bg-black bg-opacity-50 py-2">
          <p>Made with ❤️</p>
        </footer>
      </body>
    </html>
  );
}
