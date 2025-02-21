"use client";
import getArtist from "@/utils/api/artist";
import { Artist } from "@/utils/types/artist";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

const ArtistPage = () => {
  const { id } = useParams() as { id: string };
  const [artist, setArtist] = useState<Artist | null>(null);

  if (!id) {
    return (
      <div className="text-red-400 p-4 text-center">
        No artist selected. Please choose an artist.
      </div>
    );
  }

  useEffect(() => {
    getArtist(id).then((artist) => {
      setArtist(artist);
    });
  }, [id]);

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
    </div>
  );
};

export default ArtistPage;
