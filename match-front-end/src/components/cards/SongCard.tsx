"use client";
import { Song } from "@/utils/types/song";
import Link from "next/link";
import convertRuntime from "@/utils/song/runtime";

const SongCard = ({
  song,
  inline = false,
}: {
  song: Song;
  inline?: boolean;
}) => {
  const runtime = convertRuntime(Number(song.runtime));
  // inline card
  if (inline) {
    return (
      <Link
        href={`/song/${song.id}`}
        key={song.id}
        className="group select-none cursor-pointer flex items-start p-3 rounded-lg bg-white/10 hover:bg-white/20 hover:shadow-lg backdrop-blur-md transition duration-150 w-full h-[120px]"
      >
        {/* Album Cover */}
        <img
          src={song.albumCover}
          onError={(e) => {
            e.currentTarget.src = "/images/placeholder.png";
          }}
          alt={song.title}
          className="h-16 w-16 rounded-[5px] mr-[15px]"
        />

        {/* Song Info */}
        <div className="w-full flex flex-col items-start">
          <h3 className="text-xl font-bold text-orange-400 hover:text-orange-300 line-clamp-2">
            {song.title}
          </h3>

          <p className="line-clamp-1">{song.artist}</p>
          <p className="text-gray-400">{runtime}</p>
        </div>

        <div className="absolute left-0 top-0 w-full h-full p-3 bg-black/75 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-150 flex flex-col overflow-y-auto">
          <h3 className="text-xl font-bold text-orange-300">{song.title}</h3>
          <p className="text-sm">{song.artist}</p>
          <p className="text-gray-400 text-sm mt-auto">{runtime}</p>
        </div>
      </Link>
    );
  }
  // full length card
  return (
    <Link href={`/song/${song.id}`} key={song.id}>
      <div className="group select-none cursor-pointer flex items-start p-3 rounded-lg bg-white/10 hover:bg-white/20 hover:shadow-lg backdrop-blur-md transition duration-150">
        {/* Album Cover */}
        <img
          src={song.albumCover}
          alt={song.title}
          className="h-16 w-16 rounded-[5px] mr-[15px]"
          onError={(e) => {
            e.currentTarget.src = "/images/placeholder.png";
          }}
        />

        {/* Song Info */}
        <div className="w-full flex flex-col items-start">
          <h3 className="text-xl font-bold text-orange-400 hover:text-orange-300 line-clamp-2">
            {song.title}
          </h3>

          <p className="line-clamp-1">{song.artist}</p>
          <p className="text-gray-400">{runtime}</p>
        </div>
      </div>
    </Link>
  );
};

export default SongCard;
