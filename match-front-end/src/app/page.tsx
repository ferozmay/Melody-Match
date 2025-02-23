"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import SearchBar from "@/components/input/SearchBar";
import useDebounce from "@/utils/hooks/debounce";

const MusicSearchTab = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const router = useRouter();
  const debouncedSearchQuery = useDebounce(searchQuery, 250);

  useEffect(() => {
    if (debouncedSearchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  }, [debouncedSearchQuery]);

  return (
    <div className="-mt-12 h-full flex flex-col items-center justify-center bg-custom-gradient bg-fixed bg-cover">
      <div className="flex items-center gap-4 transition-transform">
        <div className="items-center px-4 py-4 ring-1 ring-gray-900/5 rounded-lg leading-none flex justify-center space-x-5">
          <img
            src="/audio-waves.png"
            alt="Logo"
            className="w-16 lg:h-36 lg:w-36"
          />
          <h1 className="text-center text-transparent text-3xl lg:text-7xl font-black animate-gradient">
            melody_match
          </h1>
        </div>
      </div>

      <SearchBar searchInput={searchQuery} setSearchInput={setSearchQuery} />
    </div>
  );
};

export default MusicSearchTab;
