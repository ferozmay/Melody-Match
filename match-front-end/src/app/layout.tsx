import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
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
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} antialiased`}
      >
        <div className="w-full bg-custom-gradient bg-fixed bg-cover min-h-screen flex items-center justify-center">
          {children}
        </div>
        {/* footer */}
        <footer className="my-12 text-center text-white text-md bg-black bg-opacity-50">
          <p>Made with ❤️ by Lauren, David, Nik, Feroz, Nuria. TTDS 2025</p>
        </footer>
      </body>
    </html>
  );
}
