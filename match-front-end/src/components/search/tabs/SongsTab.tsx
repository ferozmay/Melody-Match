import { Song } from "@/app/utils/types";
import SongCard from "@/components/cards/SongCard";
import React from "react";

interface SongsTabProps {
  results: Song[];
}

const SongsTab = ({ results }: SongsTabProps) => {
  return (
    <div>
      {results.map((song) => (
        <SongCard key={song.id} song={song} />
      ))}
    </div>
  );
};

export default SongsTab;
