import { Album } from "@/utils/types/album";
import React from "react";
import AlbumCard from "../cards/AlbumCard";

interface AlbumListProps {
  albums: Album[];
  title: string;
}

const AlbumsList: React.FC<AlbumListProps> = ({ title, albums }) => {
  return (
    <div className="w-full mt-10">
      <h2 className="text-2xl font-bold text-white mb-4">{title}</h2>
      <div className="flex flex-wrap justify-start gap-4 md:gap-6 text-white">
        {albums.slice(0, 5).map((album) => (
          <AlbumCard key={album.id} album={album} />
        ))}
      </div>
    </div>
  );
};

export default AlbumsList;
