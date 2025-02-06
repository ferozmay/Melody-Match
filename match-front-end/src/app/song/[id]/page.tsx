"use client"
import { useParams } from "next/navigation";
import useApiSearch from "@/utils/api/search";
import Link from "next/link";
import SearchBar from "@/components/input/SearchBar";

const SongPage = () => {

  
  const { id } = useParams();
  const songId = parseInt(id as string, 10);
  
  if (!id) {
    return (
      <div className="text-red-400 p-4 text-center">
        No song selected. Please choose a song.
      </div>
    );
  }

  const { query, setQuery, results } = useApiSearch();
  const song = results.songs.find((s) => s.id === songId)

  
  if (!song) {
    return (
      <div className="text-red-400 p-4 text-center">
        Song not found. Please try again.
      </div>
    );
  }

  return (

    <div className="flex flex-col items-center gap-8">
      {/* Search form
      <div className="w-full max-w-[600px]">
        <SearchBar searchInput={query} setSearchInput={setQuery} />
      </div> */}

      <div className="flex flex-col items-start justify-start w-full mt-10 md:flex-row max-w-5xl mx-auto space-y-6 md:space-y-0 md:space-x-8">
        
        {/* Album Cover */}
        <div className="w-40 h-40 md:w-60 md:h-60 flex-shrink-0 mb-6 md:mb-0">
          <img
            src={song.albumCover || "/default-cover.png"}
            alt="Album Cover"
            className="w-full h-full object-cover rounded-lg shadow-lg"
          />
        </div>

        {/* Song Info */}
        <div className="flex flex-col items-start text-white w-full">
          <h1 className="text-6xl font-extrabold text-[#ffb74d] text-left mb-4">{song.title}</h1>
          <h2 className="text-xl font-semibold text-left">{song.artist}</h2>
          <h3 className="text-lg font-semibold text-left ">{song.album}</h3>
          <p className="text-lg text-gray-400 text-left">{song.runtime}</p>
          <p className="text-lg text-gray-400 text-left mb-4">{song.topGenre || 'Unknown'}</p>

          {/* Play Button */}
          <Link href={song.link}>
            <button className="py-2 px-6 bg-[#ff0080] hover:bg-[#ff3385] text-white rounded-full font-semibold transition duration-200">
              Play Song
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SongPage;
