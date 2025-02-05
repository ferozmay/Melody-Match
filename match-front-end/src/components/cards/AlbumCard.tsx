import { Album } from "@/utils/types/album";
import React from "react";

const AlbumCard = ({ album }: { album: Album }) => {
  return (
    <div className="cursor-pointer w-52 hover:bg-white/10 bg-opacity-10 backdrop-blur-md rounded-lg hover:shadow-lg p-4 flex flex-col gap-4">
      <img
        src={album.image}
        alt=""
        className="self-center w-36 shadow-lg rounded-lg"
      />
      <div>
        <p className="text-xl font-bold text-white">
          {album.title}
        </p>
        <p className="text-gray-400">{album.artist}</p>
      </div>
    </div>
  );
};

export default AlbumCard;
