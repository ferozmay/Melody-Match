import { Song } from "@/utils/types/song";
import Link from "next/link";

const SongCard = ({ song }: { song: Song }) => {
  return (
      <div
        key={song.id}
        className="select-none cursor-pointer flex items-start p-3 rounded-lg bg-white/10 hover:bg-white/20 hover:shadow-lg backdrop-blur-md transition duration-300 w-1/3 h-full"
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
            <h3 className="text-xl font-bold text-orange-400 hover:text-orange-300">{song.title}</h3>
          </Link>
        
          <Link href={`/artist/${song.artistId}`}>
            <p className="hover:text-gray-300">{song.artist}</p>
          </Link>
          <p className="text-gray-400">{song.runtime}</p>
        </div>
        
      </div>
  );
};

export default SongCard;
