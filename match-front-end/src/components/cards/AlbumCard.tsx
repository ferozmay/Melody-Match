import { Album } from "@/utils/types/album";
import React from "react";
import Link from "next/link";

const AlbumCard = ({ album }: { album: Album }) => {
  return (
    <Link
      href={`/album/${album.id}`}
      className="cursor-pointer hover:bg-white/10 bg-opacity-10 backdrop-blur-md rounded-lg hover:shadow-lg transition duration-150 p-4 flex flex-col gap-4"
    >
      <img
        src={album.albumCover || "/images/placeholder.png"}
        alt={album.title}
        className="self-center shadow-lg rounded-lg"
        onError={(e) => {
          e.currentTarget.src = "/images/placeholder.png";
        }}
      />
      <div>
        <p className="text-xl font-bold text-white line-clamp-2">
          {album.title}
        </p>
        <p className="text-gray-400 line-clamp-1">{album.artist}</p>
      </div>
    </Link>
  );
};

export default AlbumCard;
