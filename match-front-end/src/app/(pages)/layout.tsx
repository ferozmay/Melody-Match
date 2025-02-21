import Link from "next/link";
import type { Metadata } from "next";
import Head from "next/head";
import { Inter } from "next/font/google";

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="w-full min-h-screen">
      <div className="h-20 flex items-center px-12 py-2 z-10">
        <Link href="/" className="flex items-center gap-[10px] no-underline">
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
  );
}
