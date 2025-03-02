"use client";
import AlbumsTab from "@/components/search/tabs/AlbumsTab";
import SongsTab from "@/components/search/tabs/SongsTab";
import { Album } from "@/utils/types/album";
import { Artist } from "@/utils/types/artist";
import { Song } from "@/utils/types/song";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";

type ArtistTabData = {
  songs: Song[];
  albums: Album[];
};

const TabSelector = ({
  activeTab,
  data,
}: {
  activeTab: string;
  data: ArtistTabData;
}) => {
  if (!("songs" in data)) return <></>;
  switch (activeTab) {
    case "Songs":
      return (
        <SongsTab
          results={{
            songs: data.songs,
            artists: [],
            albums: [],
            track_pages: 0,
            artist_pages: 0,
            album_pages: 0,
          }}
        />
      );
    case "Albums":
      return (
        <AlbumsTab
          results={{
            songs: [],
            artists: [],
            albums: data.albums,
            track_pages: 0,
            artist_pages: 0,
            album_pages: 0,
          }}
        />
      );
    default:
      return <></>;
  }
};

const ArtistClient = ({ artist }: { artist: Artist }) => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const selectedTab = searchParams.get("tab") || "Songs";
  const tabs = ["Songs", "Albums"];
  const [activeTab, setActiveTab] = useState<string>(selectedTab);

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    router.push(`/artist/${artist?.id}?tab=${tab}`);
  };

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="flex flex-col items-start justify-start w-full mt-10 md:flex-row max-w-5xl mx-auto space-y-6 md:space-y-0 md:space-x-8">
        {/* Artist Image */}
        <div className="w-40 h-40 md:w-60 md:h-60 flex-shrink-0 mb-6 md:mb-0">
          <img
            src={artist?.artistImage || "/images/placeholder.png"}
            alt="Artist Image"
            className="w-full h-full object-cover rounded-lg shadow-lg"
          />
        </div>

        {/* Artist Info */}
        <div className="flex flex-col items-start text-white w-full">
          <h1 className="text-6xl font-extrabold text-orange-400 text-left mb-4">
            {artist?.name}
          </h1>
          <p className="text-lg text-gray-400 text-left">
            {artist?.bio || "Artist bio is not available."}
          </p>
        </div>
      </div>
      <div className="w-full my-5 max-w-5xl flex flex-col gap-4">
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
        <TabSelector
          activeTab={activeTab}
          data={{ albums: artist?.albums || [], songs: artist?.songs || [] }}
        />
      </div>
    </div>
  );
};

export default ArtistClient;
