"use client";
import { playerStore } from "@/components/common/PlayerControls";
import SongsList from "@/components/common/SongsList";
import convertRuntime from "@/utils/song/runtime";
import { Song } from "@/utils/types/song";
import Link from "next/link";
import React from "react";

const SongClient = ({ song }: { song: Song }) => {
  const togglePlaying = playerStore((state) => state.togglePlaying);
  const isPlaying = playerStore((state) => state.isPlaying);

  return (
    <div className="flex flex-col items-center gap-8">
      {/* Search form
      <div className="w-full max-w-[600px]">
        <SearchBar searchInput={query} setSearchInput={setQuery} />
      </div> */}

      <div className="flex flex-col items-start justify-start w-full mt-10 md:flex-row max-w-5xl mx-auto space-y-6 md:space-y-0 md:space-x-8">
        {/* Album Cover */}
        <div className="w-40 h-40 md:w-60 md:h-60 flex-shrink-0 mb-6 md:mb-0">
          <img
            src={song?.albumCover || "/images/placeholder.png"}
            alt={song?.title}
            className="w-full h-full object-cover rounded-lg shadow-lg"
            onError={(e) => {
              e.currentTarget.src = "/images/placeholder.png";
            }}
          />
        </div>

        {/* Song Info */}
        <div className="flex flex-col items-start text-white w-full">
          <h1 className="text-6xl font-extrabold text-orange-400 text-left mb-4">
            {song?.title}
          </h1>
          <Link href={`/artist/${song?.artistId}`}>
            <h2 className="text-xl font-semibold text-white hover:text-gray-200 text-left">
              {song?.artist}
            </h2>
          </Link>
          <Link href={`/album/${song?.albumId}`}>
            <h3 className="text-lg text-gray-200 hover:text-gray-300 text-left ">
              {song?.album}
            </h3>
          </Link>
          <p className="text-lg text-gray-400 text-left">
            {convertRuntime(Number(song?.runtime))}
          </p>
          <p className="text-lg text-gray-400 text-left mb-4">
            {song?.topGenre || "Unknown"}
          </p>

          {/* Play Button */}
          <button
            className="py-2 px-6 bg-pink-600 hover:bg-pink-500 text-white rounded-full font-semibold transition duration-200"
            onClick={(e) => {
              e.stopPropagation();
              togglePlaying();
            }}
          >
            {isPlaying ? "Pause" : "Play"}
          </button>
        </div>
      </div>
      <div className="w-full my-10 max-w-5xl mx-10  md:space-x-8">
        {/* Display similar songs */}
        <SongsList title="Similar Songs" songs={song?.similarSongs || []} />
      </div>
    </div>
  );
};

export default SongClient;
