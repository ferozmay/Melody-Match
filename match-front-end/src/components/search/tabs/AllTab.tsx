import { Song } from "@/app/utils/types";
import AlbumCard from "@/components/cards/AlbumCard";
import ArtistCard from "@/components/cards/ArtistCard";
import SongCard from "@/components/cards/SongCard";
import { Artist } from "@/utils/types/artist";
import React from "react";

interface AllTabProps {
  results: {
    songs: Song[];
    artists: Artist[];
    albums: {
      id: number;
      title: string;
      artist: string;
      cover: string;
      link: string;
    }[];
  };
}

const AllTab = ({ results }: AllTabProps) => {
  return (
    <div className="w-full py-8 pb-12 flex flex-col gap-8">
      {Object.keys(results).map((key) => (
        <div key={key} className="flex flex-col gap-3">
          <p className="text-4xl font-bold text-left capitalize">{key}</p>
          <div className="flex gap-5">
            {results[key].length > 0 ? (
              results[key].map((result, idx) => {
                switch (key) {
                  case "songs":
                    return (
                      <SongCard key={`${key}-${idx}-${result}`} song={result} />
                    );

                  case "artists":
                    return (
                      <ArtistCard
                        key={`${key}-${idx}-${result}`}
                        artist={result}
                      />
                    );
                  case "albums":
                    return (
                      <AlbumCard
                        key={`${key}-${idx}-${result}`}
                        album={result}
                      />
                    );
                }
              })
            ) : (
              <p>No results found.</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AllTab;
