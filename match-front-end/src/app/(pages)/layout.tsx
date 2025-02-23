import Link from "next/link";

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="w-full min-h-screen">
      <div className="h-20 flex items-center px-4 lg:px-12 py-2 z-10">
        <Link href="/" className="flex items-center gap-4 no-underline">
          <img
            src="/audio-waves.png"
            alt="Melody Match Logo"
            className="h-12 lg:h-20 w-auto"
          />
          <h2 className="m-0 lg:text-3xl font-black animate-gradient">
            melody_match
          </h2>
        </Link>
      </div>
      <div className="px-4 ">{children}</div>
    </div>
  );
}
