import ArtistCard from "@/components/cards/ArtistCard";
import { Artist } from "@/utils/types/artist";

const ArtistsTab = ({ results }: { results: Artist[] }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
      {results.map((artist, idx) => (
        <ArtistCard key={`artist-${idx}-${artist.id}`} artist={artist} />
      ))}
    </div>
  );
};

export default ArtistsTab;
