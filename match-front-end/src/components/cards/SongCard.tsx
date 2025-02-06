import { Song } from "@/app/utils/types";
import Link from "next/link";

const SongCard = ({ song }: { song: Song }) => {
  return (
    <div
      key={song.id}
      className="select-none h-full flex items-start p-3 rounded-lg bg-white/10"
    >
      {/* Album Cover */}
      <img
        src={song.albumCover}
        alt="Album Cover"
        className="my-auto h-16 w-16 rounded-[5px] mr-[15px]"
      />
      {/* Song Info */}
      <div className="w-full flex flex-col items-start">
        <Link href={`/song/${song.id}`}>
          <h3 className="text-xl font-bold text-[#ffb74d]">{song.title}</h3>
        </Link>
        <p className="">{song.artist}</p>
        <p className="text-gray-400">{song.runtime}</p>
      </div>
      {/* View Details Button */}
      <Link
        href={`/song/${song.id}`}
        className="self-end no-underline bg-[#ff0080] text-white py-[8px] px-[15px] rounded-[5px] transition-colors duration-300 hover:bg-[#ff3385]"
      >
        View Details
      </Link>
    </div>
  );
};

export default SongCard;
