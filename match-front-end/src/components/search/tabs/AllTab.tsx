import AlbumCard from "@/components/cards/AlbumCard";
import ArtistCard from "@/components/cards/ArtistCard";
import SongCard from "@/components/cards/SongCard";
import { Album } from "@/utils/types/album";
import { Artist } from "@/utils/types/artist";
import { SearchResults } from "@/utils/types/searchResults";
import { Song } from "@/utils/types/song";
import React from "react";

interface AllTabProps {
  results: SearchResults;
}

const AllTab = ({ results }: AllTabProps) => {
  return (
    <div className="w-full py-8 pb-12 flex flex-col gap-8">
      {/* explicit array for order */}
      {(["songs", "albums", "artists"] as (keyof SearchResults)[]).map(
        (key) => (
          <div key={key} className="flex flex-col gap-3">
            <p className="text-4xl font-bold text-left capitalize">{key}</p>
            <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-4">
              {results[key] && results[key].length > 0 ? (
                results[key].slice(0, 6).map((result, idx) => {
                  switch (key) {
                    case "songs":
                      return (
                        <SongCard
                          inline
                          key={`${key}-${idx}-${result}`}
                          song={result as Song}
                        />
                      );
                    case "albums":
                      return (
                        <AlbumCard
                          key={`${key}-${idx}-${result}`}
                          album={result as Album}
                        />
                      );
                    case "artists":
                      return (
                        <ArtistCard
                          key={`${key}-${idx}-${result}`}
                          artist={result as Artist}
                        />
                      );
                  }
                })
              ) : (
                <p>No results found.</p>
              )}
            </div>
          </div>
        )
      )}
    </div>
  );
};

export default AllTab;
