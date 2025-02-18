import { Artist } from "@/utils/types/artist";
import React from "react";
import Link from "next/link";

const ArtistCard = ({ artist }: { artist: Artist }) => {
  return (
    <Link href={`/artist/${artist.id}`} className="cursor-pointer w-52 hover:bg-white/10 bg-opacity-10 backdrop-blur-md rounded-lg hover:shadow-lg transition duration-300 p-4 flex flex-col gap-4">
      <img src={artist.image} alt="" className="self-center w-36 shadow-lg rounded-full" />
      <p className="text-xl text-center font-bold text-white">{artist.name}</p>
    </Link>
  );
};

export default ArtistCard;
