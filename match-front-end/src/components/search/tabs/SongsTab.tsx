import SongCard from "@/components/cards/SongCard";
import { Song } from "@/utils/types/song";
import React from "react";

interface SongsTabProps {
  results: Song[];
}

const SongsTab = ({ results }: SongsTabProps) => {
  return (
    <div className="w-full grid grid-cols-1 gap-4">
      {results.map((song) => (
        <SongCard key={song.id} song={song} />
      ))}
    </div>
  );
};

export default SongsTab;
