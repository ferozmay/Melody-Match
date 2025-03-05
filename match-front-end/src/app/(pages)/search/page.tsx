"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import SearchBar from "@/components/input/SearchBar";
import useApiSearch from "@/utils/api/search";
import AllTab from "@/components/search/tabs/AllTab";
import SongsTab from "@/components/search/tabs/SongsTab";
import { SearchResults } from "@/utils/types/searchResults";
import ArtistsTab from "@/components/search/tabs/ArtistsTab";
import AlbumsTab from "@/components/search/tabs/AlbumsTab";
import paginatorStore, { PaginatorStoreProps } from "@/utils/store/paginator";

const TabSelector = ({
  activeTab,
  results,
}: {
  activeTab: string;
  results: SearchResults;
}) => {
  if (!("songs" in results)) return <></>;
  switch (activeTab) {
    case "All":
      return <AllTab results={results} />;
    case "Songs":
      return <SongsTab results={results} />;
    case "Artists":
      return <ArtistsTab results={results} />;
    case "Albums":
      return <AlbumsTab results={results} />;
    default:
      return <></>;
  }
};

const SearchResultsComponent = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  //   const searchQuery = searchParams.get("q") || "";
  const selectedTab = searchParams.get("tab") || "All";

  const tabs = ["All", "Songs", "Artists", "Albums", "Lyrics"];
  const [activeTab, setActiveTab] = useState<string>(selectedTab);
  const activeTabPage = paginatorStore(
    (state: PaginatorStoreProps) => state.activePage
  );
  const setActiveTabPage = paginatorStore(
    (state: PaginatorStoreProps) => state.setActivePage
  );

  const { query, setQuery, results, loading } = useApiSearch();

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    setActiveTabPage(1);
  };

  useEffect(() => {
    router.push(`/search?q=${query}&tab=${activeTab}&page=${activeTabPage}`);
  }, [activeTabPage, query, activeTab]);

  useEffect(() => {
    if (searchParams.get("tab")) {
      handleTabChange(searchParams.get("tab") || "All");
    }
    if (searchParams.get("q")) {
      setQuery(searchParams.get("q") || "");
    }
    if (searchParams.get("page")) {
      setActiveTabPage(Number(searchParams.get("page") || 1));
    }
  }, [searchParams]);

  useEffect(() => {
    if (query) {
      router.push(`/search?q=${query}&tab=${activeTab}&page=${activeTabPage}`);
    }
  }, [query]);

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="lg:w-[80%] mx-auto text-white">
        {/* search results bar */}
        <div className="w-full flex flex-col lg:flex-row justify-start gap-6">
          {/* Search settings */}
          <div className="w-full flex flex-col gap-2 max-w-[650px]">
            {/* Search form input */}
            <div className="w-full">
              <SearchBar searchInput={query} setSearchInput={setQuery} />
            </div>
            <h1 className="text-2xl font-bold">
              Search results for:{" "}
              <span className="text-[#ffb74d]">{query}</span>
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
          {/* player controls */}
          {/* <div className="w-full h-full ">
            
          </div> */}
        </div>
        {/* /search bar */}
        {/* Search results */}
        <div className="w-full flex justify-center py-4 lg:py-8">
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
};

export default function SearchResultsPage() {
  return (
    <Suspense>
      <SearchResultsComponent />
    </Suspense>
  );
}
