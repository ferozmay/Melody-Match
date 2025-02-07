import { Song } from "@/app/utils/types";
import Link from "next/link";

const SongCard = ({ song }: { song: Song }) => {
  return (
    <div
      key={song.id}
      className="select-none flex items-start p-3 rounded-lg bg-white/10 w-1/3 h-full"
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
      
    </div>
  );
};

export default SongCard;
