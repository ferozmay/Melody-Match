import AlbumCard from "@/components/cards/AlbumCard";
import Paginator from "@/components/common/Paginator";
import { Album } from "@/utils/types/album";
import { SearchResults } from "@/utils/types/searchResults";

const AlbumsTab = ({ results }: { results: SearchResults }) => {
  return (
    <div className="w-full flex flex-col gap-8">
      <div className="grid grid-cols-2 md:grid-cols-4 2xl:grid-cols-5 gap-4">
        {results.albums?.map((album: Album, idx: number) => (
          <AlbumCard key={`album-${idx}-${album.id}`} album={album} />
        ))}
      </div>
      <Paginator totalPages={results.album_pages || 0} />
    </div>
  );
};

export default AlbumsTab;
