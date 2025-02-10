import { Artist } from "@/utils/types/artist";
import React from "react";

const ArtistCard = ({ artist }: { artist: Artist }) => {
  return (
    <div className="cursor-pointer w-52 hover:bg-white/10 bg-opacity-10 backdrop-blur-md rounded-lg hover:shadow-lg p-4 flex flex-col gap-4">
      <img src={artist.image} alt="" className="self-center w-36 shadow-lg rounded-full" />
      <p className="text-xl text-center font-bold text-white">{artist.name}</p>
    </div>
  );
};

export default ArtistCard;
