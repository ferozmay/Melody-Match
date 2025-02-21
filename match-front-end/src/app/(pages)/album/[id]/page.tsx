"use client";
import { useParams } from "next/navigation";
import useApiSearch from "@/utils/api/search";
import Link from "next/link";
import SimilarSongs from "@/components/SimilarSongs";
import SearchBar from "@/components/input/SearchBar"; // Optional, if you want a search bar

const AlbumPage = () => {
  const { id } = useParams();
  const albumId = parseInt(id as string, 10);

  if (!id) {
    return (
      <div className="text-red-400 p-4 text-center">
        No album selected. Please choose an album.
      </div>
    );
  }

  const { query, setQuery, results } = useApiSearch();
  const album = results.albums.find((a) => a.id === albumId);

  if (!album) {
    return (
      <div className="text-red-400 p-4 text-center">
        Album not found. Please try again.
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="flex flex-col items-start justify-start w-full mt-10 md:flex-row max-w-5xl mx-auto space-y-6 md:space-y-0 md:space-x-8">
        {/* Album Image */}
        <div className="w-40 h-40 md:w-60 md:h-60 flex-shrink-0 mb-6 md:mb-0">
          <img
            src={album.image || "/default-album.png"}
            alt="Album Cover"
            className="w-full h-full object-cover rounded-lg shadow-lg"
          />
        </div>

        {/* Album Info */}
        <div className="flex flex-col items-start text-white w-full">
          <h1 className="text-6xl font-extrabold text-orange-400 text-left mb-4">
            {album.title}
          </h1>
          <Link href={`/artist/${album.artistId}`}>
            <h2 className="text-xl font-semibold text-white hover:text-gray-200 text-left">
              {album.artist}
            </h2>
          </Link>

          {album.releaseDate && (
            <p className="text-md text-gray-500 mt-2">
              Released: {album.releaseDate}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlbumPage;
