import { Song } from "@/utils/types/song";
import SongCard from "../cards/SongCard";

interface SongsListProps {
  songs: Song[];
  title: string;
}

const SongsList = ({ songs, title }: SongsListProps) => {
  return (
    <div className="w-full mt-10">
      <h2 className="text-2xl font-bold text-white mb-4">{title}</h2>
      <div className="flex flex-wrap justify-start gap-4 md:gap-6 text-white">
        {songs.slice(0, 5).map((song) => (
          <SongCard key={song.id} song={song} />
        ))}
      </div>
    </div>
  );
};

export default SongsList;
