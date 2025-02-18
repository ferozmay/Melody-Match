import SongCard from "./cards/SongCard";
import { Song } from "@/app/utils/types";

interface SimilarSongsProps {
  similarSongs: Song[];
}

const SimilarSongs = ({ similarSongs }: SimilarSongsProps) => {
  return (
    <div className="w-full mt-10">
      <h2 className="text-2xl font-bold text-white mb-4">Similar Songs</h2>
      <div className="flex flex-wrap justify-start gap-6 md:gap-8 text-white">
        {similarSongs.slice(0, 3).map((song) => (
          <SongCard key={song.id} song={song} />
        ))}
      </div>
    </div>
  );
};

export default SimilarSongs;
