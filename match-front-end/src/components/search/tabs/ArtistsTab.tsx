import ArtistCard from "@/components/cards/ArtistCard";
import Paginator from "@/components/common/Paginator";
import { Artist } from "@/utils/types/artist";
import { SearchResults } from "@/utils/types/searchResults";

const ArtistsTab = ({ results }: { results: SearchResults }) => {
  return (
    <div className="w-full flex flex-col gap-8">
      <div className="grid grid-cols-2 lg:grid-cols-4 2xl:grid-cols-5 gap-4">
        {results.artists.map((artist: Artist, idx: number) => (
          <ArtistCard key={`artist-${idx}-${artist.id}`} artist={artist} />
        ))}
      </div>
      <Paginator totalPages={results.artist_pages || 0} />
    </div>
  );
};

export default ArtistsTab;
