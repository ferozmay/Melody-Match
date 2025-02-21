"use client";
import { useParams } from "next/navigation";
import Link from "next/link";
import { useEffect, useState } from "react";
import { Album } from "@/utils/types/album";
import getAlbum from "@/utils/api/album";

const AlbumPage = () => {
  const { id } = useParams() as { id: string };
  const [album, setAlbum] = useState<Album | null>(null);

  if (!id) {
    return (
      <div className="text-red-400 p-4 text-center">
        No album selected. Please choose an album.
      </div>
    );
  }

  useEffect(() => {
    getAlbum(id).then((album: Album) => {
      setAlbum(album);
    });
  }, [id]);

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="flex flex-col items-start justify-start w-full mt-10 md:flex-row max-w-5xl mx-auto space-y-6 md:space-y-0 md:space-x-8">
        {/* Album Image */}
        <div className="w-40 h-40 md:w-60 md:h-60 flex-shrink-0 mb-6 md:mb-0">
          <img
            src={album?.albumCover || "/image/placeholder.png"}
            alt="Album Cover"
            className="w-full h-full object-cover rounded-lg shadow-lg"
          />
        </div>

        {/* Album Info */}
        <div className="flex flex-col items-start text-white w-full">
          <h1 className="text-6xl font-extrabold text-orange-400 text-left mb-4">
            {album?.title}
          </h1>
          <Link href={`/artist/${album?.id}`}>
            <h2 className="text-xl font-semibold text-white hover:text-gray-200 text-left">
              {album?.artist}
            </h2>
          </Link>

          {album?.releaseDate && (
            <p className="text-md text-gray-500 mt-2">
              Released: {album?.releaseDate}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlbumPage;
