import { Artist } from "@/utils/types/artist";
import React from "react";
import Link from "next/link";

const ArtistCard = ({ artist }: { artist: Artist }) => {
  return (
    <Link
      href={`/artist/${artist.id}`}
      className="cursor-pointer w-full hover:bg-white/10 bg-opacity-10 backdrop-blur-md rounded-lg hover:shadow-lg transition duration-150 p-4 flex flex-col gap-4"
    >
      <img
        src={artist.artistImage}
        alt={artist.name}
        className="self-center shadow-lg rounded-full"
        onError={(e) => {
          e.currentTarget.src = "/images/placeholder.png";
        }}
      />
      <p className="text-xl text-center font-bold text-white line-clamp-2">
        {artist.name}
      </p>
    </Link>
  );
};

export default ArtistCard;
