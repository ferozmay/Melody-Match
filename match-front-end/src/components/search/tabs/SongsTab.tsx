import SongCard from "@/components/cards/SongCard";
import Paginator from "@/components/common/Paginator";
import { SearchResults } from "@/utils/types/searchResults";
import { Song } from "@/utils/types/song";
import React from "react";

interface SongsTabProps {
  results: SearchResults;
}

const SongsTab = ({ results }: SongsTabProps) => {
  return (
    <div className="w-full flex flex-col gap-8">
      <div className="w-full grid grid-cols-2 lg:grid-cols-4 2xl:grid-cols-4 gap-4">
        {results.songs.map((song) => (
          <SongCard key={song.id} song={song} />
        ))}
      </div>
      <Paginator totalPages={results.track_pages || 0} />
    </div>
  );
};

export default SongsTab;
