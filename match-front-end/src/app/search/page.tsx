"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import SearchBar from "@/components/input/SearchBar";
import useApiSearch from "@/utils/api/search";
import AllTab from "@/components/search/tabs/AllTab";
import SongsTab from "@/components/search/tabs/SongsTab";

const TabSelector = ({ activeTab, results }) => {
  switch (activeTab) {
    case "All":
      return <AllTab results={results} />;
    case "Songs":
      return <SongsTab results={results.songs} />;
    default:
      return <></>;
  }
};

export default function SearchResultsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  //   const searchQuery = searchParams.get("q") || "";
  const selectedTab = searchParams.get("tab") || "All";

  const tabs = ["All", "Songs", "Artists", "Albums", "Lyrics"];
  const [activeTab, setActiveTab] = useState<string>(selectedTab);

  const { query, setQuery, results, loading } = useApiSearch();

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    router.push(`/search?tab=${tab}`);
  };

  useEffect(() => {
    if (searchParams.get("tab")) {
      handleTabChange(searchParams.get("tab") || "All");
    }
  }, [searchParams]);

  return (
    <div className="flex flex-col items-center gap-8">
      {/* Search form */}
      <div className="w-full max-w-[600px]">
        <SearchBar searchInput={query} setSearchInput={setQuery} />
      </div>
      <div className="w-[80%] mx-auto text-white">
        {/* Search settings */}
        <div className="px-5 flex flex-col gap-2">
          <h1 className="text-2xl font-bold">
            Search results for: <span className="text-[#ffb74d]">{query}</span>
          </h1>
          {/*  */}
          <div className="text-md flex w-full h-10 gap-3 flex-wrap">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => handleTabChange(tab)}
                className={` py-1 px-4 border rounded ${
                  activeTab == tab
                    ? "bg-white text-black"
                    : "bg-transparent text-white hover:bg-white/10"
                } duration-150`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
        {/* Search results */}
        <div className="w-full flex justify-center">
          {loading ? (
            <div className="h-48 flex items-center my-auto text-orange-400 text-3xl">
              Loading...
            </div>
          ) : (
            <TabSelector activeTab={activeTab} results={results} />
          )}
          {/* /results */}
        </div>
      </div>
    </div>
  );
}
